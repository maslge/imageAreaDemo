# imageAreaDemo

1. index.html : example imageMapping avec JS et utilisant bootstrap
2. fab : evolution du 1 avec jquery
3. caption.html : plus d'image mapping un image sur laquelle on place des buttons et on declanche par JS l'affichage d'un fenetre d'info, ...
4. captionFullCss.html : idem 3 mais sans JS ! full CSS et declenchement sur hover

## Hosting AWS
via service
```
https://lightsail.aws.amazon.com/ls/webapp/account/keys
```

```bash
bitnami@ip-172-26-1-32
ssh bitnami@18.197.40.62
```

dans le rep nginx du host
```
/opt/bitnami/nginx/html/dofin
```

## Test CircleCi

###Installation
```bash
sudo curl -fLSs https://circle.ci/cli | bash
mv circleci ~/products/circleci/
```

### Ajouter dans le PATH
```bash
export PATH=$PATH:/home/bdarras/products/circleci
```

### execution en local du job
```bash
circleci local execute --job build-and-test
```
