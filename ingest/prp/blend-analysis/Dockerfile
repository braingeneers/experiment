FROM python:latest

RUN pip install numpy matplotlib boto3 --upgrade Pillow
RUN yes | apt-get update
RUN yes | apt-get install vim
RUN pip install --upgrade git+https://github.com/braingeneers/braingeneerspy.git

COPY upload_feature.py ./upload_feature.py
COPY download_batch.py ./download_batch.py
COPY make_blend_analysis.py ./make_blend_analysis.py
COPY blend-this.jpg ./blend-this.jpg

CMD ["python3"]     
