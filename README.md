# imageAreaDemo


## test CircleCi

###Installation
sudo curl -fLSs https://circle.ci/cli | bash
mv circleci ~/products/circleci/

### Ajouter dans le PATH
export PATH=$PATH:/home/bdarras/products/circleci

### execution en local du job
circleci local execute --job build-and-test
