# Why run Kubernetes jobs?

If someone has an amazing new analysis that they want to use on the data, they would have to recreate the same analysis on each new data set. They could give me their analysis to automate into ingest, but then I would have to take the time to understand the analysis in order to correctly and efficiently automate it, while also downloading the right packages. With the kubernetes jobs, one can automatically upload the analysis they want done, and then have it done with all subsequent data sets. 

## Getting Started Part 1: Git Clone and Adding your scripts

In order to first begin making your analysis job, git clone the experiment/ingest/prp/example-spikes/ folder. You will not need to alter the download_batch.py file, which will automatically download batch for the ingest. You will need to replace the make_example_spikes.py with a script that can take an environment variable called "UUID" and output the results of your analysis into a folder like /public/groups/braingeneers/ephys/UUID/example_spikes/. After that you will have to change the file from saving to /public/groups/braingeneers/ephys/$UUID/example_spikes/ to /public/groups/braingeneers/ephys/$UUID/{your analysis name}/. Then you must alter upload_feature.py to upload to that directory as well. 

## Getting Started Part 2: Alter Dockerfile and Create Image
Make sure you add RUN commands in your Dockerfile in case you need other packages for your analysis.
On the command line run this in the same directory to build and push your image:
<pre><code>
docker build -t {username}/{name_for_your_image} .
docker push {username}/{name_for_your_image}:latest 
</code></pre>

## Getting Started Part 3: Alter .yaml file

Make sure you alter the yaml file to work for your docker image like the example below:
<pre><code>
containers:
  - name: example-spikes
    image: {username}/{name_for_your_image}:latest
    imagePullPolicy: Always
</code></pre>

You should also alter the name:
<pre><code>
apiVersion: batch/v1
kind: Job
metadata:
  name: {your analysis name}
spec:
</code></pre>

## Getting Started Part 4: Test Out Your Kubernetes Container

In order to test your Kubernetes container, set
<pre><code>
command: ["/bin/bash", "-c" ]
args:
 - sleep 3h
</code></pre>

Use one of the test UUID cases with:

<pre><code>
export UUID="5000-00-00-e-stuff"
</code></pre>

Create your container with:
<pre><code>
envsubst < example-spikes.yaml | kubectl create -f -
</code></pre>

Locate your pod with:
<pre><code>
kubectl get pods
</code></pre>

Jump into your pod with:
<pre><code>
kubectl exec -it example-spikes-vxjfw bash
</code></pre>

From there you can run your scripts to make sure they work: <pre><code> download_batch.py && python3 make_example_spikes.py && python3 upload_feature.py</code></pre>

## Getting Started Part 5: Final Touches and Push to Github

Once you have tested everything, and you are sure that everything works make sure your args look like this so everything can run automatically:
<pre><code>
command: ["/bin/bash", "-c" ]
  args:
    - python3 download_batch.py && python3 make_example_spikes.py && python3 upload_feature.py
  env:
</code></pre>

Add only your yaml file to experiment/ingest/prp/jobs/ephys/ and it will be automatically incorporated into the next ingest.










