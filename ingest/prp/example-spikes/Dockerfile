FROM python:latest                                                                                                                    
                                           
COPY upload_feature.py ./upload_feature.py                                                                                            
COPY download_batch.py ./download_batch.py                                                                                            
COPY make_example_spikes.py ./make_example_spikes.py                                                                                  
                                                                                                                                                                                                                                                                            RUN pip install numpy                                                                                                                 
RUN pip install spikeinterface                                                                                                        
RUN pip install matplotlib                                                                                                            
RUN pip install ml_ms4alg                                                                                                             
RUN pip install boto3                                                                                                                 
RUN yes | apt-get update                                                                                                              
RUN yes | apt-get install vim                                                                                                         
RUN pip install --upgrade git+https://github.com/braingeneers/braingeneerspy.git                                                      
                        
CMD ["python3"]     
