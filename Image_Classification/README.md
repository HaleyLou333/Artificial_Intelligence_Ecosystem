# AI Image Processing and Classification Project

This project is designed to give you hands-on experience working with an image classifier and enhancing your programming skills using AI assistance. The project has two parts, each focused on different aspects of image classification and processing. By the end, you'll have explored fundamental concepts like Grad-CAM, image classification, and creative image filtering.

## Table of Contents 

1. [Project Overview](#project-overbiew)
2. [Image Used](#image-used)
3. [Top 3 Predictions](#top-3-predictions)
4. [Line-by-Line Code Explanation](#line-by-line-code-explanation)
5. [Reflection](#reflection)
6. [Grad-CAM Visualization](#grad-cam-visualization)
7. [Creative Filter Experiment](#creative-filter-experiment)
8. [Conclusion](#conslution)

---

## Project Overview
This project explores how a pretrained MobileNetV2 model classifies images and how interpretability tools like Grad-CAM help reveal what the model is focusing on. The assignment includes:
- Running a basic classifier
- Understanding the code through AI explanation
- Reflecting on the model's behavior 
- Generating a Grad-CAM heatmap
- Applying a creative image filter

---

## Image Used
'toni-cuenca-unsplash.jpg'

---

## Top-3 Predictions

1. Hamster (0.09)
2. Arctic_fox (0.03)
3. Hen (0.03)

---

## Line-by-Line Code Explanation

I asked AI (Co-Pilot) to explain the 'base_classifier.py' script.
Here is a summary of what each part does:

- **Imports TensorFlow, Keras utilities, and NumPy**
These libraries handle the model, image loading, preprocessing, and numerical operations.
Example: `import tensorflow as tf`

- **Loads the pretrained MobileNetV2 model**
The model come with ImageNet weights, giving it knowledge of 1,000 object categories.
Example: `model = MobileNetV2(weights="imagenet")`

- **Defines a function to classify an image**
This function loads the image, resizes it, converts it to an array, preprocesses it, runs the model, and prints the top-3 predictions. Example: `img = image.load_img(image_path, target_size=(224, 224))`

- **Uses a loop to classify multiple images**
The script continues to ask for filenames until the user types 'exit'.
Example: `while True:`

- **Includes error handling**
If the image path is wrong or unreadable, the script prints an error instead of crashing.
Example: `except Exception as e:`

## Reflection

Running the basic classifier helped me understand how a pretrained model processes an image from start to finish. The AI's explanation made the flow of the program feel intuitive: load the image, preprocess it, expand the dimensions, run the model, decode the predictions, and print the results. Even though I'm still building confidence with Python, the explanation made the logic feel approachable instead of abstract. What suprised me most was how much preprocessing matters. I hadn't fully appreciated that the model expects images in a very specific format, and that a single step like 'preprocess_input' is doing a lot of invisible work. The predictions also showed how these models latch onto textures and shapes more than the "meaning" of the object. My photo of a little chick being classified as a hamster actually made sense once I looked at the fluffy texture and round shape.

---

## Grad-CAM Visualization
Grad-CAM can be added by accessing the final convolutional layer of MobileNetV2, computing the gradient of the predicted class with respect to that layer’s feature maps, and combining them to create a heatmap. The heatmap is then resized and overlaid on the original image to show which regions influenced the model’s decision. This requires modifying the classifier to extract intermediate activations and gradients during prediction.

## Understanding the Grad-CAM Algorithm
To better understand how the classifier makes decisions, I asked AI to explain the Grad-CAM algorithm.

**What Grad-CAM Does**
Grad-CAM (Gradient-weighted Class Activation Mapping) is a visualization technique that highlights the regions of an image that most strongly influence a model's prediction. It produces a heatmap that can be overlaid on the original image to reveal where the model is "looking".

**How the Algorithim Works**
1. **Forward Pass**
The image is passed through the model to obtain a prediction and identify the top predicted class.

2. **Select the Last Convolutional Layer**
Grad-CAM uses the final convolutional layer because it retains spatial information that fully connected layers lose.

3. **Compute Gradients**
The gradient of the predicted class score is computed with respect to the feature maps of the last conv layer. These gradients indicate how important each feature map is for the prediction.

4. **Global Average Pooling**
The gradients are averaged across spatial dimensions to produce a weight for each feature map.

5. **Weighted Combination**
Each feature map is multiplied by its corresponding weight and summed to create a coarse heatmap.

6. **ReLU Activation**
Negative values are removed, keeping only features that positively contribute to the prediction.

7. **Upsampling & Overlay**
The heatmap is resized to match the original image and blended on top, revealing the regions the model focused on.

## Heatmap Analysis
After integrating Grad-CAM into the classifier, I generated a heatmap for the same chick image used earlier.

**What the Heatmap Shows**
- Higher activation around the outer edges of the image  
- Lower activation across the chick’s body, with its outline still faintly visible  
- Minimal activation on the head, eyes, and feathers compared to the high‑contrast background  

**Interpretation**
The Grad-CAM output shows that the model's strongest gradient responses occured in the high-contrast background rather than on the chick itself. This suggests that the final convolutional layer produced a coarse or noisy activations, causing the model to emphasize edges and color transisions more than the subject. Even so, the chick's outline is still visible in cooler colors, indicating that the model did register the presence of the bird, just with the lower intensity compared to the surrounding background.

**Conclusion**
Overall, the Grad-CAM visualization reveals that while the classifier does not detect the chick, its attention is not strongly centered on the most semantically meaningful regions of the image. Instead, the model's gradients are dominated by the bright, stylized background. This highlights a limitation of Grad-CAM on images with heavy color effects or soft subject contrast, and it suggests that additional preprocessing or fine-tuning could help the model focus more reliably on the intended object.

---

## Creative Filter Experiment
*(To be added after running basic_filter.py)*

Include:
- The filtered image
- Applied effect
- Reason for choice
- How the filter changed the model's predictions (if applicable)

---

## Conclusion
This project has helped me to understand both the strengths and limitations of pretrained image classifiers. Running the model, interpreting its predictions, and visualizing its attention through Grad-CAM made the process feel more transparent and less like a black box. The creative filter experiement also showed how small visual changes can shift the model's perception.