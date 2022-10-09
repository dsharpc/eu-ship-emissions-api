
docker build -t eu.gcr.io/c-chain-test/api:$1 --target prod ./api/
docker push eu.gcr.io/c-chain-test/api:$1