#!/bin/bash

login="à_changer"
remoteFolder="/tmp/$login/"
fileName="server"
fileExtension=".py"
#écrire la liste des noms ou IP des machines utilisées selon qu'il y est un DNS utilisé pour leur noms
computers=("nom_machine1" "nom_machine2" "nom_machine3")

for c in ${computers[@]}; do
  command0=("ssh" "$login@$c" "lsof -ti | xargs kill -9")
  command1=("ssh" "$login@$c" "rm -rf $remoteFolder;mkdir $remoteFolder")
  command2=("scp" "$fileName$fileExtension" "$login@$c:$remoteFolder$fileName$fileExtension")
  command3=("ssh" "$login@$c" "cd $remoteFolder;python3 $fileName$fileExtension")
  echo ${command0[*]}
  "${command0[@]}"
  echo ${command1[*]}
  "${command1[@]}"
  echo ${command2[*]}
  "${command2[@]}"
  echo ${command3[*]}
  "${command3[@]}" &
done
