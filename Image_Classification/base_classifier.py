import tensorflow as tf
tf.get_logger().setLevel('ERROR')
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input, decode_predictions
from tensorflow.keras.preprocessing import image
import numpy as np

# Grad-CAM Function
def generate_gradcam(image_path, model, last_conv_layer_name="Conv_1"):
# load and preprocess image
    img = image.load_img(image_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = preprocess_input(img_array)
    img_array = np.expand_dims(img_array, axis=0)

    # get model prediction
    preds = model.predict(img_array)
    pred_index = np.argmax(preds[0])

    # get last convolutional layer
    last_conv_layer = model.get_layer(last_conv_layer_name)

    # build a model that maps input -> activation + prediction
    grad_model = tf.keras.models.Model(
        [model.inputs],
        [last_conv_layer.output, model.output]
    )

    # compute gradients
    with tf.GradientTape() as tape:
        conv_outputs, predictions = grad_model(img_array)
        loss = predictions[:, pred_index]

    grads = tape.gradient(loss, conv_outputs)

    # compute channel-wise mean of gradients
    pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))

    # weigh conv outputs by gradients
    conv_outputs = conv_outputs[0]
    heatmap = conv_outputs @ pooled_grads[..., tf.newaxis]
    heatmap = tf.squeeze(heatmap)

    # normalize heatmap
    heatmap = tf.maximum(heatmap, 0) / tf.math.reduce_max(heatmap)

    return heatmap.numpy()

def save_and_display_gradcam(image_path, heatmap, alpha=0.4):
    import matplotlib.cm as cm
    import cv2

    # load original image
    img = image.load_img(image_path)
    img = image.img_to_array(img)
    
    # convert original image to uint8
    img = np.uint8(img)

    # resize heatmap to match image size
    heatmap = cv2.resize(heatmap, (img.shape[1], img.shape[0]))

    # convert heatmap to RGB using colormap
    heatmap = np.uint8(255 * heatmap)
    colormap = cm.jet(heatmap)[:, :, :3]

    # convert colormap to uint8
    colormap = np.uint8(colormap * 255)

    # overlay heatmap on original image
    superimposed_img = cv2.addWeighted(img, 1 - alpha, colormap, alpha, 0)

    # save and display
    output_path = "gradcam_output.jpg"
    cv2.imwrite(output_path, superimposed_img)

    print(f"Grad_CAM saved to {output_path}")

# Load Model
model = MobileNetV2(weights="imagenet")



# Basic Classifier Function
def classify_image(image_path):
    try:
        img = image.load_img(image_path, target_size=(224, 224))
        img_array = image.img_to_array(img)
        img_array = preprocess_input(img_array)
        img_array = np.expand_dims(img_array, axis=0)

        predictions = model.predict(img_array)
        decoded_predictions = decode_predictions(predictions, top=3)[0]

        print("\nTop-3 Predictions for", image_path)
        for i, (_, label, score) in enumerate(decoded_predictions):
            print(f"  {i + 1}: {label} ({score:.2f})")
    except Exception as e:
        print(f"Error processing '{image_path}': {e}")

# Main Program Loop
if __name__ == "__main__":
    print("Image Classifier (type 'exit' to quit, or 'gradcam' to generate a heatmap)\n")

    while True:
        image_path = input("Enter image filename: ").strip()

        # Exit option
        if image_path.lower() == "exit":
            print("Goodbye!")
            break

        # Grad-CAM option
        if image_path.lower() == "gradcam":
            target = input("Enter image filename for Grad-CAM: ").strip()
            try:
                heatmap = generate_gradcam(target, model)
                save_and_display_gradcam(target, heatmap)
            except Exception as e:
                print(f"Error generating Grad-CAM: {e}")
            continue

        # Normal classification
        classify_image(image_path)
