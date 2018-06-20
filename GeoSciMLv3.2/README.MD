# OWL generation from GeoSciML 3.2

During the Vancouver meeting, it was suggested to use GeoSciML 3.2 to generate the OWL because it had less XSD artefacts (specially the Description classes use to hook extension).

## artefacts

This folder should contain a zipped version of the model (GeoSciMLv3.2_unversioned.EAP.zip that Steve uploaded).  The .sh unzips the archive before processing it (to avoid having a large EAP file in git).  It removes the previous .EAP if any (so, if you unzip and make changes to the EAP, change the name.. or the script) and then removes it when ShapeChange is done.

This .sh runs in GitBash, and assumes you have a have a ShapeChange installed on /c/sc.  Also assumes running on Windows (because there is a java dll bridge to read the eap file, so.).  It also assumes ```SSJavaCOM.dll``` is in ```/c/sc/lib/```

launch the script in GitBash with

``` ./gsml3owl.sh ```

If it does not work, maybe you need to

```chmod +x gsml3owl.sh```


### gsml3owl.sh

```sh
rm GeoSciMLv3.2_unversioned.EAP
unzip  GeoSciMLv3.2_unversioned.EAP
java -Djava.library.path=/c/sc/lib/ -jar /c/sc/ShapeChange-2.5.0.jar   -Dfile.encoding=UTF-8 -c sc/gsml3.xml
rm GeoSciMLv3.2_unversioned.EAP
```

## files

The config file is in ```/sc``` folder.  This is also where ShapeChange will output the result (it creates an INPUT folder)

### 2018-06-20 :

I just slightly modified ```gsmlb.xml``` to create ```sc/gsml3.xml```  and gave it a go.  The log file in /sc reports a lot of errors, so this is the next step - go through the list.
