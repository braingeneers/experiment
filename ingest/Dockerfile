FROM python:latest

RUN pip install numpy spikeinterface matplotlib ml_ms4alg boto3
RUN yes | apt-get update && yes | apt-get install vim gettext-base awscli
RUN curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add - && \
	echo "deb http://apt.kubernetes.io/ kubernetes-xenial main" > /etc/apt/sources.list.d/kubernetes.list && \
	apt-get update && \
	apt-get install -y kubectl

COPY prp_ingest.py ./prp_ingest.py
COPY 256ANS_locs.csv ./256ANS_locs.csv
COPY read_data.py ./read_data.py
COPY grab_files_from_derived.py ./grab_files_from_derived.py
COPY intanutil ./intanutil
COPY upload_to_prp.py ./upload_to_prp.py
COPY send_me_to_prp.txt ./send_me_to_prp.txt
COPY download_from_prp.py ./download_from_prp.py
COPY check_for_dir_change_in_pod.sh ./check_for_dir_change_in_pod.sh
COPY create_current_files_in_dir.py ./create_current_files_in_dir.py
COPY create_files_in_dir.py ./create_files_in_dir.py 
COPY download_files_in_dir.py ./download_files_in_dir.py
COPY automation_in_pod.sh ./automation_in_pod.sh
COPY run_jobs.sh ./run_jobs.sh
COPY pull_git_jobs.sh ./pull_git_jobs.sh
COPY run_ingest.sh ./run_ingest.sh

CMD ["python3"]
