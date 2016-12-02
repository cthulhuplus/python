#!/usr/bin/python
import os, os.path, sys, argparse, re

parser = argparse.ArgumentParser()

parser.add_argument("-a", "--account", dest="account", help="All CMS on specified cPanel account")
parser.add_argument("-w", "--wordpress", "--wp", dest="wordpress", help="Targets Wordpress installations", action='store_true')
parser.add_argument("-j", "--joomla", dest="joomla", help="Targets Joomla installations", action='store_true')
parser.add_argument("-d", "--drupal", dest="drupal", help="Targets Drupal installations", action='store_true')
parser.add_argument("-e", "--exhaustive", dest="exhaustive", help="All supported CMS on All Accounts", action='store_true')


args = parser.parse_args()

acctPath = "/home/{0}/public_html".format(args.account)

#Joomla - CMS Script style output
def jooVphp():
  fileList = []
  for root, folders, files in os.walk(acctPath):
    for file in files:
      if file == 'version.php':
        fileList.append(os.path.join(root,file))

  for path in fileList:
    with open(path) as f:
      for line in f:
        if "public $RELEASE = '" in line:
          version_number = line[20:25]
          inst_path = re.sub('libraries/cms/version/version.php', '', path)
          version_number = re.sub('\';', '', version_number)
#          print "Joomla installation(s) and version(s):"
          print inst_path + " = " + version_number + " Joomla"
          
          #Wordpress - CMS Script style output
def wpVphp():
  fileList = []
  for root, folders, files in os.walk(acctPath):
    for file in files:
      if file == 'version.php':
        fileList.append(os.path.join(root,file))

  for path in fileList:
    with open(path) as f:
      for line in f:
        if line.startswith("$wp_version ="):
          version_number = line[15:20]
          inst_path = re.sub('wp-includes/version.php', '', path)
          version_number = re.sub('\';', '', version_number)
#          print "Wordpress installation(s) and version(s):"
          print inst_path + " = " + version_number + " Wordpress"

#Drupal - CMS Script style output
def druVphp():
  fileList = []
  for root, folders, files in os.walk(acctPath):
    for file in files:
      if file == 'bootstrap.inc':
        fileList.append(os.path.join(root,file))

  for path in fileList:
    with open(path) as f:
      for line in f:
        if "define('VERSION', '" in line:
          version_number = line[19:26]
          inst_path = re.sub('includes/bootstrap.inc', '', path)
          version_number = re.sub('\'\);', '', version_number)
#          print "Drupal installation(s) and version(s):"
          print inst_path + " = " + version_number + " Drupal"

#Exhaustive - CMS Script style output
fullList = []

#Exhaustive - CMS Script style output
def exhaustive():
  cpdir = "/var/cpanel/users"
  druList = []
  wpList = []
  jooList = []

  for root, folders, files in os.walk(cpdir):
    for file in files:
      newpath = "/home/" + os.path.join(file) + "/public_html/"
      if "public_html" in newpath:

###Wordpress
        for root, folders, files in os.walk(newpath):
          for file in files:
            if file == 'version.php':
              wpList.append(os.path.join(root,file))

        for path in wpList:
          with open(path) as f:
            for line in f:
              if line.startswith("$wp_version ="):
                version_number = line[15:20]
                inst_path = re.sub('wp-includes/version.php', '', path)
                version_number = re.sub('\';', '', version_number)
#                print inst_path + " = " + version_number + " Wordpress"
#                 return inst_path + " = " + version_number + " Wordpress"
                fullList.append(inst_path + " = " + version_number + " Wordpress")

###Joomla
        for root, folders, files in os.walk(newpath):
          for file in files:
            if file == 'version.php':
              jooList.append(os.path.join(root,file))

        for path in jooList:
          with open(path) as f:
            for line in f:
              if "public $RELEASE = '" in line:
                version_number = line[20:25]
                inst_path = re.sub('libraries/cms/version/version.php', '', path)
                version_number = re.sub('\';', '', version_number)
#                print inst_path + " = " + version_number + " Joomla"
#               return inst_path + " = " + version_number + " Joomla"
                fullList.append(inst_path + " = " + version_number + " Joomla")
                
                ###Drupal
        for root, folders, files in os.walk(newpath):
          for file in files:
            if file == 'bootstrap.inc':
              druList.append(os.path.join(root,file))

        for path in druList:
          with open(path) as f:
            for line in f:
              if "define('VERSION', '" in line:
                version_number = line[19:26]
                inst_path = re.sub('includes/bootstrap.inc', '', path)
                version_number = re.sub('\'\);', '', version_number)
#                print inst_path + " = " + version_number + " Drupal"
#               return inst_path + " = " + version_number + " Drupal"
                fullList.append(inst_path + " = " + version_number + " Drupal")

###Uniqify
  output = []
  for each in fullList:
    if each not in output:
      output.append(each)
  print ("\n".join(output))

#Actions
if args.wordpress:
  print "Wordpress installation(s) and version(s):"
  wpVphp()
elif args.joomla:
  print "Joomla installation(s) and version(s):"
  jooVphp()
elif args.drupal:
  print "Drupal installation(s) and version(s):"
  druVphp()
elif args.exhaustive:
  print "Exhaustive installation(s) and versions(s):"
  exhaustive()
else:
  print "Too bad, so sad."
