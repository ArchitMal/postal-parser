

CLUSTER_NAME=postal-parser
REGION=us-central1
BUCKET_NAME=postal-parser


gcloud config set dataproc/region ${REGION}

echo "Creating a cluster"

gcloud beta dataproc clusters create ${CLUSTER_NAME} \
	--region ${REGION} \
	--metadata 'PIP_PACKAGES=google-cloud-storage spark-nlp==2.5.1' \
	--worker-machine-type e2-standard-8 \
	--num-workers 2 \
	--image-version 1.4-debian10 \
	--initialization-actions gs://dataproc-initialization-actions/python/pip-install.sh \
	--optional-components=JUPYTER,ANACONDA \
	--enable-component-gateway \
	--max-idle="10m" \
	--bucket=${BUCKET_NAME} 

echo "Listing clusters that exist"

gcloud dataproc clusters list

echo "Submitting the job"

gcloud dataproc jobs submit pyspark \
       	--cluster ${CLUSTER_NAME} \
       	--properties=spark.jars.packages=com.johnsnowlabs.nlp:spark-nlp_2.11:2.5.1 \
	--driver-log-levels root=FATAL \
	pyspark_sa.py \
	-- ${BUCKET_NAME}

