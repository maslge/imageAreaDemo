# interactive Images project
```
.
├── build # archive de webcontent
│   └── dofin.tgz
├── deploy # script de deploiement sur AWS
│   ├── deployOnRemoteHost.sh
│   └── deploy.sh
├── Dockerfile
├── exampleConf # example de configuration
│   ├── toolchainA.CSV
│   ├── toolchainA.json
│   └── toolchainA.yaml
├── interactiveImageGenerator.py # generator script
├── README.md
├── requirements.txt
├── templateCaptionFullCss.html
├── templateCaptionFullCssPageHTML.html
├── templateIndex.html
├── Upload_Here_Config_To_Generate_WebSite # repertoire source pour la generation du site
│   ├── Toolchain.NET.IIS.ITCLOUD.png
│   └── toolchain.NET.IIS.ITCloud.xml
└── webContent # contenu du site web post genration
    ├── caption.css
    ├── devopsCredito.png
    ├── Dofin.jpg
    ├── index.html
    ├── toolchain.NET.IIS.ITCloud.html
    └── Toolchain.NET.IIS.ITCLOUD.png

```
## usage
1. setup configuration file & png images in Upload_Here_Config_To_Generate_WebSite dir (xml + png)
2. launch generation interactiveImageGenerator.py
3. browse web site generated from webContent

### configuration files
see exampleConf for example of configuration either in xml, csv or json Upload_Here_Config_To_Generate_WebSite directory

# How to build your own set of interactive Images

## how to integrate my own image 

Create your own conf (xml, json or CSV) + image for each interactive image in 

### First - Editing your image with GIMP to scale & get coordinates for pins

Picture need to be scaled in order to fit your need in the final rendering, to proceed :  

1. with Gimp edit your image and scale it to the right size :

`Gimp menu > Image > Scale 1200 px` 

`<picture file="Toolchain.NET.IIS.ITCLOUD.png" width="1200px" />` 
   
(image sizing recommendation 1200px) 

2. select position (mouse position is given by Gimp : bottom/left of the screen)  for caption with the mouse and start editing the xml description file

Important note : Coordinate for the right positioning of the caption is (not the center of the caption) TOP + LEFT  

example 

```
    <caption posx="420px" posy="121px">
		<popup>
			<headerText>Orchestrator Jenkins</headerText>
			<bodyhtml><![CDATA[
				L'orchestrateur est la pièce centrale de la plateforme d'integration continue car
				c'est le moteur qui va lancer succèssivement toutes les phases permettant le build
				de l'application <img src="build.png" width="50px" height="50px">
				 (recuperation du code dans Git, la compilation des sources, les test unitaires, les quality gates ...
				 pour finalement uploader le livrable war, ... dans le repo d'arctifact nexus.<br/>
				 Jenkins est le produit qui joue ce role d'orchestrateur chez PF aujourd'hui, lien pour accèder à <a href="http://devpico-pfc.rb.echonet">jenkins</a>
			]]></bodyhtml>
			<footertext>footer</footertext>
		</popup>
	</caption>
```

3. complete your xml doc with documentation for each caption and upload everything in the Uploadxxx Dir
4. launch generator
5. Browse and check result in webContent (nginx, Httpd, ...) 

# Build & Hosting : CircleCI + Hosting AWS
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
