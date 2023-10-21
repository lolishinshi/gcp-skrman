FUNCTION_NAME=skrman
REGION=us-east1
USEROUTPUT=false

# TODO: 用 gcloud 的 secret 来存储 token

deploy:
	pdm export -f requirements > requirements.txt
	gcloud functions deploy $(FUNCTION_NAME) \
		--gen2 \
		--runtime python311 \
		--memory 256MiB \
		--timeout 30s \
		--set-env-vars "BOT_TOKEN=${BOT_TOKEN},DATABASE_URL=${DATABASE_URL}" \
		--region $(REGION) \
		--source=. \
		--entry-point handler \
		--trigger-http \
		--user-output-enabled=$(USEROUTPUT)

delete:
	gcloud functions delete $(FUNCTION_NAME) --region $(REGION)