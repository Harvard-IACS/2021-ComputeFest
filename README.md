# 2021 IACS ComputeFest

# ComputeFest Videos
[January 19th Tuesday Morning](https://harvard.zoom.us/rec/share/1vRaQNVCgZ69fGg9K98F9SoSlgz3iTOpD7HTpFD_tSToq_g_onUSzIPLndaxX2q5.OXnnK6l4f2sG93us) - 
[January 19th Tuesday Afternoon](https://harvard.zoom.us/rec/share/rpu8Chtpv7oVYpXNdwBK1xPhyIE4uR-DMMY3SM6-hEg1dKgzpeNaWjrj9hosJGDO.DD1aYyieR2VjQ1aT)

[January 20th Wednesday Morning](https://harvard.zoom.us/rec/share/3cisw4RBDKDWLX0j0F_q6Pmy9-XTEJgHEGd-Ve3YvodPlKPAyolkP_9aVEQL1hAT.WArYO2Br98ngtJ1u?startTime=1611154931000) - 
[January 20th Wednesday Afternoon](https://harvard.zoom.us/rec/share/2c1-KPljv05oa33XmJgbKaJ4RneFwdx-NzDdHKAFaQv78sQu6BSz1lLcFTN-ABbI.3D3-O5K1ml1m22hT?startTime=1611167499000)

[January 21st Thursday Morning](https://harvard.zoom.us/rec/share/Bg0lQ4zqdit7nysCz7enTd8kz_qBVYx3p8yAA359kE5dhQXbuk8mh7BwhH3YpmkP.13ahCQ4RefEfKdR4) - 
[January 21st Thursday Afternoon](https://harvard.zoom.us/rec/share/7vnr67X_XVuzKgb9jILmhJYCEqr-SX6-X_QYIh1_DuiB4aMIN5rkVjSwx-PBYbsF.wJGTxQO00-Y0ewPm?startTime=1611253924000)

[January 22nd Friday Morning](https://harvard.zoom.us/rec/share/RFA69-Rb-zoY_VLDb4YwD1iUKJ0LUZP4oQtVMQnLzSP-swy9QwOvKj4uMNLszeju.DNnG9BTGvQo0jWC1?startTime=1611327707000) - 
[January 22nd Friday Afternoon](https://harvard.zoom.us/rec/share/gkiq_L0bChhw8FUj704LpnIoLVP_ZTv7kjqrJi1rvzzA1zotrBZ6fXvV_3JGMLM_.XRttfMxtxTTEINr5?startTime=1611340332000)


## Woof Woof! - Project Details

### Background
For Computefest 2021, Harvard IACS will be creating hands-on workshops that will be an in-depth tutorial on transfer learning for computer vision and language models, building applications using deep learning models and deploying them in production. The outcome of the four days workshop will be to build a full featured application for the Austin Pets Alive (APA). APA is an association of pet owners for pet owners. Our goal will be to build a reusable application, design, and framework that can be used in any animal welfare nonprofits to connect future pet owners with pets.

### Problem Statement
For the scope of the workshops we will focus on creating a user friendly tool that helps connect future dog owners with dogs available for adoption. The core problem we are trying to solve is to help future dog owners find a dog who is a good fit for their lifestyle and family environment. First we help the user search for dogs based on certain features such as size and color. Secondly we will connect the dog with the user by allowing the user to chat with a persona of the dog. The user can ask this virtual dog any question about it, its breed characteristics, or any general questions about puppies and dogs.


### Workshop Workflow

![docker_container_diagram](./woof-woof-app/imgs/workshop_flow.png)

#### Build Vision Models:
Workshop will be an in-depth tutorial on transfer learning for computer vision. Will cover state of the art models and how to perform transfer learning in general with practical examples. Topics that will be covered:

**Concepts**:
- CNNs
- Transfer learning
- SOTA models
- Network distillation

**Workshops**:
- Image classification
- Feature extraction
- Create embeddings
- Distillation

#### Build Language Models:
Workshop will be an in-depth tutorial on transfer learning for natural language. Will cover state of the art models and how to perform transfer learning in general with practical examples. Topics that will be covered:

**Concepts**:
- Seq2Seq
- Attention & Self-attention
- Transformers
- Transfer learning
- SOTA models

**Workshops**:
- Language models
- Question answering models
- Dialog models

#### Notebook to App:
Workshop will be an in-depth tutorial on bringing code from notebooks to self contained environments. Will cover different options for python environments with a primary focus on containerized development. Topics that will be covered:

**Concepts**:
- Virtual environments
- Virtual machines
- Containers
- Microservices/APIs

**Workshops**:
- Code optimization
- Creating Docker containers
- Building and running the app containers

#### Deployment:
Workshop will be an in-depth tutorial on deploying containers to the AWS cloud environment. Topics that will be covered:

**Concepts**:
- Amazon Web Services (AWS)
- AWS Classrooms
- Kubernetes

**Workshops**:
- Setup Kubernetes cluster
- Deploy app to AWS


### App Design

![docker_container_diagram](./woof-woof-app/imgs/woof-woof-app-mockup.png)

#### Flow:
- User can find dogs using “Find me” filters
- Select one or more dogs to find dogs similar to the selected ones
- Select a dog to chat with. This opens up a personalized chatbot for the selected dog


**Home Page**:
- Default page when app starts up
- Top “n” dogs shown by default
- Image card displays name and image of dog
- Image cards are selectable (multiple)
- “Find Similar” button shows up when one or more image cards are selected

**Find me Search/Filter**:
- The search/filter section will stay on each page
- Allows filter by:
    - Breed 
    - Age (range)
    - Height (range)
    - Weight (range)
- Similar - an image upload to find dogs similar to the dog in the uploaded picture
The filter will get applied on change of any of the filter elements and refresh the image grid

**Select a dog to chat with it**:
- Image cards in the image grid display a “chat” icon for each dog
- Click on “chat” icon to open up a chat popup
- The chatbot active will be specific to the dog selected
- Dog chat bot can answer basic question about itself + other general questions about the breed + some general question about dogs

### Solution Architecture

![solution_architecture](./woof-woof-app/imgs/solution_architecture.png)

**Process**:
- Data Scientists can perform model training
- Users can view dogs available for adoption
- Users can search for dogs based on various filter conditions
- User can select a dog and “talk” to it

**Colab**:
- Web based hosted notebook solution from Google with access to GPU for model training

**Frontend**:
- User friendly single page app with capabilities to view and search dogs
- Chatbot

**Backend**:
- API Server to expose dog metadata
- Embedding Search service to find images that are similar to a give image or images
- Model Serving to serve the models for inference 

**Data**:
- Local file or database store
- Cloud data store
- Cloud model store


### Technical Architecture

![technical_architecture](./woof-woof-app/imgs/technical_architecture.png)

**Colab**:
- Google Colab will be used for model training of image and language models
- Trained models will be saved in AWS S3 buckets

**Elastic Container Registry (ECR)**:
- ECR Hub will be used to host all the container images

**AWS S3 Bucket Store**:
- S3 buckets will be used as a common storage repositories for data, embeddings, and models

**Kubernetes Cluster**:
- Kubernetes cluster will be used to deploy the various containers on AWS




