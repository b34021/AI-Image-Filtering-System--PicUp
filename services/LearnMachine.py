#llm

# import tensorflow as tf
# from tensorflow.keras.models import Sequential
# from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
# from tensorflow.keras.preprocessing.image import ImageDataGenerator
#
# # הגדרת נתיב לתמונות
# train_dir = 'path_to_train_data'
# validation_dir = 'path_to_validation_data'
#
# # הגדרת ImageDataGenerator להכנה וטעינת נתונים
# train_datagen = ImageDataGenerator(rescale=1./255, horizontal_flip=True, rotation_range=20)
# test_datagen = ImageDataGenerator(rescale=1./255)
#
# train_generator = train_datagen.flow_from_directory(
#     train_dir,
#     target_size=(150, 150),
#     batch_size=32,
#     class_mode='categorical'
# )
#
# validation_generator = test_datagen.flow_from_directory(
#     validation_dir,
#     target_size=(150, 150),
#     batch_size=32,
#     class_mode='categorical'
# )
#
# # יצירת מודל CNN
# model = Sequential()
#
# # הוספת שכבות קונבולוציה ומדגם
# model.add(Conv2D(32, (3, 3), activation='relu', input_shape=(150, 150, 3)))
# model.add(MaxPooling2D((2, 2)))
#
# model.add(Conv2D(64, (3, 3), activation='relu'))
# model.add(MaxPooling2D((2, 2)))
#
# model.add(Conv2D(128, (3, 3), activation='relu'))
# model.add(MaxPooling2D((2, 2)))
#
# # שטח שטוח לפני השכבה המלאה
# model.add(Flatten())
#
# # הוספת שכבות fully connected
# model.add(Dense(512, activation='relu'))
# model.add(Dropout(0.5))
# model.add(Dense(5, activation='softmax'))  # 5 קטגוריות
#
# # קימפול המודל
# model.compile(loss='categorical_crossentropy',
#               optimizer='adam',
#               metrics=['accuracy'])
#
# # אימון המודל
# history = model.fit(
#     train_generator,
#     steps_per_epoch=100,
#     epochs=10,
#     validation_data=validation_generator,
#     validation_steps=50
# )
#
# # שמירת המודל
# model.save('wedding_image_classifier.h5')