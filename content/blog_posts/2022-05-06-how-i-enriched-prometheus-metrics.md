---
title: "How I enriched prometheus metrics"
summary: VMWare exporter metrics didn't have all the informations we wanted. This is how I enriched them.
cover: "2022-05-06.jpg"
cover_alt: "how i enriched prometheus metrics article cover"
date: 2022-05-05
tags: [prometheus, python, pandas, dataframe, vmware, exporter, vmware_exporter, fastapi]
---

## Context

In my current mission, in order to set up a metric-federation, we have to gather vmware metrics.

So we used the [vmware_exporter](https://github.com/pryorda/vmware_exporter) by [Daniel Pryor](https://github.com/pryorda), and to not edit it, i wrote a small front made with fastapi.

Metrics are get by fastapi, parsed, enriched, reserialized, and scrapped by prometheus.

Metrics names need to be mapped, as they are unified with metrics from openstack and IBM cloud.

MapTable is the one below :

<pre class="blockquotecode my-4 py-3">
<code>MAPPING_METRICS_NAME = {
    "vmware_vm_power_state" : "power_state"
    "vmware_vm_cpu_usage_average"': "cpu_usage_percentage
    "vmware_vm_mem_consumed_average": "memory_used"
    "vmware_vm_memory_max": "memory_total"
    "vmware_vm_mem_usage_average": "memory_usage_percentage",
    "vmware_vm_num_cpu": "vcpus"
}</code></pre>

## Step1 : Parsing vmware_exporter metrics

Exporter is hit from within a function named request_exporter().

The output of the exporter is one big str file that need to be parsed in order to be processed.

I used prometheus_client.parser for this.

<pre class="blockquotecode my-4 py-3">
<code>from prometheus_client.parser import text_string_to_metric_families

data_from_exporter = request_exporter(target)
metric_families = text_string_to_metric_families(data_from_exporter)</code>
</pre>

The variable metric_families is a multilevel object containing metrics grouped by metric name.

It can be represented as a dict, where key is the metric_name and the value is a list containing all metrics as tuples.

Example : 
<pre class="blockquotecode my-4 py-3">
<code>{
    "vmware_vm_power_state": [
        ("vmware_vm_power_state", {"vm_name": "vm1", "label2": "value2"}, 1),
        ("vmware_vm_power_state", {"vm_name": "vm2", "label2": "value2"}, 0),
    ]
}</code>
</pre>

So I made a little algorithm to flatten the object as a list of dicts :

<pre class="blockquotecode my-4 py-3">
<code>processed_exporter_data = []

for family in data_from exporter:
    if family.name not in MAPPING_METRICS_NAME:
        continue
    for sample in family.samples:
        row dict = {}
        row dict["__name__"] = sample[0]
        for key, value in sample[1].items():
            row dict[key] = value
        row_dict["value"] = sample[2]
        processed exporter_data.append(row_dict)</code>
</pre> 

I will have then a list of dicts, a dataframe can be created out of it.

<pre class="blockquotecode my-4 py-3">
<code>[
    {"__name__": "vmware_vm_power_state", "vm_name": "vm1", "value": 1},
    {"__name__": "vmware_vm_power_state", "vm_name": "vm2", "value": 0},
]</code>
</pre>

Now let's play with dataframe ...

## Step2: Playing with dataframes

First of all, i'm creating the dataframe :

<pre class="blockquotecode my-4 py-3">
<code>import pandas

metrics_df = pandas.DataFrame(processed_exporter_data)</code>
</pre>

Then, I am purging the uneeded labels :

<pre class="blockquotecode my-4 py-3">
<code>metrics_df.drop(
    colums=[
        "host_name",
        "ds_name",
        "dc_name",
        "cluster_name",
    ],
    axis=1,
    inplace=True,
)</code>
</pre>

This way, I am using the dataframe to delete the 4 columns, <code>inplace=True</code> is used in order to overwrite existing dataframe and not create a new one.

Then i have to merge metric data with data from two other internal datasources (one for the hosts/vm referential, one for the business lines). 

These are also represented as dataframes.

<pre class="blockquotecode my-4 py-3">
<code>businesslines_referential_df = referential_df.merge(
    businesslines_df, how="left", left_on="ecosystem", right_index=True
)</code>
</pre>

This merge will enrich referential dataframe with businesslines data, from right to left, according to ecosystem name and use the index from the right dataframe as the join key.

Now it is time to merge this dataframe with the metrics dataframe.

<pre class="blockquotecode my-4 py-3">
<code>metrics_df = metrics_df.merge(
    businesslines_referential_df, how="inner", left_on="vm_name", right_index=True
)</code>
</pre>

This merge is made with the inner method, so this way we only keep common columns, according to vm_name.

Now i'm replacing original metric name with the mapping we talked about earlier :

<pre class="blockquotecode my-4 py-3">
<code>metrics_df.replace({"__name_": MAPPING_METRICS_NAME}, inplace=True)</code>
</pre>

Now "vmware_vm_power_state" is mapped to "power_state".

The result is similar to this :

<table width="100%" border="1px">
    <tr>
        <th>__name__</th>
        <th>vm_name</th>
        <th>ecosystem</th>
        <th>business_line</th>
        <th>value</th>
    </tr>
    <tr>
        <td>power_state</td>
        <td>vm1</td>
        <td>TESTECO</td>
        <td>BL1</td>
        <td>1</td>
    </tr>
</table>

Now to be scrapped by prometheus that data needs to be reserialized.

## Step3: How i re-serialized data ?

Prometheus Metrics strings are pretty simple :

<code>metric_name{label1="value1", label2="value2"} 0</code>

Using list comprehension i am iterating over the dataframe to print a string containing in the begining the metric_name and in the end the metric_value.

<pre class="blockquotecode my-4 py-3">
<code>return "\n".join(
    [
        f"{row['__name__']}{generate_dict_label(row)} {row['value']}"
        for index, row in metrics df.iterrows()
    ]
)</code>
</pre>

The tricky thing to do is to generate labels stuff, because we cannot tweak output of a dict in python.

Dict in python look like <code>{"key": "value"}</code>, we have to generate a string that look like <code>{label="value"}</code>

So I wrote a little function that generate that string.

<pre class="blockquotecode my-4 py-3">
<code>def generate_dict_label(row):

    labels = set(row.index) - {"__name__", "value"}

    return (
        "{"
        + ",".join(
            [
                f'{key}="{value}"'
                for key, value in row.items()
                if key in labels
            ]
        )
        + "}"
    )</code>
</pre>

Finally, serialized data looks like :

<pre class="blockquotecode my-4 py-3">
<code>
power_state{vm_name="vm1", ecosystem="TESTECO", business_line="BL1"} 1
</code>
</pre>

Now, metrics are scrapped by prometheus calling a small module made with fastapi, that will parse, enrich, and reserialize data, that comes from a prometheus vmware exporter.