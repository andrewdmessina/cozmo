# cozmo
In order to use this to train a MobileNet Tensorflow Graph go into the scripts folder
and type "python3 retrain.py --object_name [new object to train for]".  Cozmo will then
take pictures for 10 seconds and then rebuild the graph in order to account for the new 
object.  

retrain.py also has many more options available and they are well documented, so feel
free to tweak as you need to.