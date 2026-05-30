from ultralytics import YOLO

model = YOLO("yolov8s.pt")

results=model.train(
    data="Users/svbachiraju/Documents/Closet-Backend/outfit-generator/dataset",
    epochs=10, #number of trainign round/numbe rof times model looks at each image. higher numbers might lead ot overfitting
    imgsz=600, #all images aere sized to 600*600
    batch=16, #set to -1 for mdoel to find largest batch size model cna handle withotu crashing
    device='cpu', #computer uses GPU for trianing claultions, instead of CPU or aother
    project="outfit-generator", 
    name="training_performance"
)




