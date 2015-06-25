import exifread
import os
import re
import simplekml

def getFileNames():
	fileNameList = []
	prog = re.compile(r".jpg")
	dir = os.listdir(os.getcwd())
	for img in dir:
		if re.search(prog,img.lower()):
			fileNameList.append(img)
	return fileNameList

def pullTags(fileName):
	f = open(fileName,'rb')
	tags = exifread.process_file(f)
	exportTags = ['GPS GPSLongitude','GPS GPSLongitudeRef', 'GPS GPSLatitude', 'GPS GPSLatitudeRef','EXIF DateTimeDigitized']
	#'GPS GPSImgDirectionRef','GPS GPSImgDirection' These can be added if found to be useful.
	value = []
	for tag in exportTags:
		if tag not in ('JPEGThumbnail', 'TIFFThumbnail', 'Filename', 'EXIF MakerNote'):
			value.append(tags[tag])
	for index in range(0,len(value)-1):
		if index == 0 or index == 2:
			value[index] = formatCoor(value[index])
			if (str(value[index+1]) == "S") or (str(value[index+1]) == "W"):
				value[index] = value[index]*-1.0
			value[index] = str(value[index])
	value.remove(value[1])
	value.remove(value[2])
	value[2] = value[2].values
	return value

def formatCoor(rawCoor):
	return (((rawCoor.values[2].num / float(rawCoor.values[2].den))/60.0) + rawCoor.values[1].num)/60.0 + float(rawCoor.values[0].num)


fileNameList = getFileNames()
f = open('EXIF_GPS.txt','w')
for file in fileNameList:
	listVals = pullTags(file) # Need to convert 0 and 2
	bufferString = file + ", " + listVals[0] + ", " + listVals[1] + ", " + listVals[2] + "\n"
	f.write(bufferString)
	kml = simplekml.Kml()
	kml.newpoint(name=file[:-4],coords=[(listVals[0],listVals[1])])
	kml.save(file[:-4] + '.kml')
	print "%s coordinates have been added" % (file)
f.close()



