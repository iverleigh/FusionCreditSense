FROM continuumio/miniconda3

RUN conda create --name finclude python=3.7
RUN conda install pandas
RUN conda install scikit-learn
RUN conda install -c anaconda ipykernel
RUN conda install -c anaconda flask
RUN conda install -c conda-forge matplotlib

RUN mkdir /code
WORKDIR /code
COPY . /code/

EXPOSE 8001
CMD python /code/webapp/Flask.py --host=0.0.0.0 --port=8001