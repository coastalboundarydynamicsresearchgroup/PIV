import cv2
import numpy as np

def findGreenSpecs(imagePath, outputImagePath):
    image = cv2.imread(imagePath)
    hsvImage = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    lowerGreen = np.array([40, 50, 50])  
    upperGreen = np.array([80, 255, 255])

    # Create a mask for green color
    greenMask = cv2.inRange(hsvImage, lowerGreen, upperGreen)

    # Find contours in the mask
    contours, _ = cv2.findContours(greenMask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # List to store coordinates of green specs
    greenSpecsCoordinates = []

    for contour in contours:
        if cv2.contourArea(contour) > 1:  # Ignore very small specs (adjust threshold as needed)
            x, y, w, h = cv2.boundingRect(contour)
            greenSpecsCoordinates.append((int(x + w / 2), int(y + h / 2)))  # Center of the bounding box
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)  

    # Save the output image with red boxes
    cv2.imwrite(outputImagePath, image)

    return greenSpecsCoordinates

# Main function to test the program
if __name__ == "__main__":
    # Input and output file paths
    inputImagePath = "path/to/your/image.jpg"  # Replace with your image path
    outputImagePath = "path/to/output/image_with_boxes.jpg"  # Replace with desired output path
    
    # Call the function and get the coordinates
    coordinates = findGreenSpecs(inputImagePath, outputImagePath)

    # Print the coordinates of green specs
    print("Green Specs Coordinates:", coordinates)
    print(f"Output image saved to: {outputImagePath}")
