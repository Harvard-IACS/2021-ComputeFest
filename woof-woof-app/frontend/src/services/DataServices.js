const axios = require('axios');

const HOSTNAME_TAG = "<hostname>"
//const BASE_API_URL = process.env.REACT_APP_API_BASE_URL;
let BASE_API_URL = process.env.REACT_APP_BASE_API_URL;
let BASE_EMBEDDING_URL = process.env.REACT_APP_BASE_EMBEDDING_URL;
let BASE_MODEL_URL = process.env.REACT_APP_BASE_MODEL_URL;

if(BASE_API_URL.includes(HOSTNAME_TAG)){
    //window.location.hostname
    BASE_API_URL = BASE_API_URL.replace(HOSTNAME_TAG, window.location.hostname);
    BASE_EMBEDDING_URL = BASE_EMBEDDING_URL.replace(HOSTNAME_TAG, window.location.hostname);
    BASE_MODEL_URL = BASE_MODEL_URL.replace(HOSTNAME_TAG, window.location.hostname);
}

//axios.defaults.baseURL = BASE_API_URL;
console.log(process.env);
console.log(BASE_API_URL);
console.log(BASE_EMBEDDING_URL);
console.log(BASE_MODEL_URL);


const DataServices = {
    Init: function(){
        // Any application initialization logic comes here
    },
    GetDogs : async function(breed){
        return await axios.get(BASE_API_URL+"/dogs?breed="+breed);
    },
    GetBreeds : async function(){
        return await axios.get(BASE_API_URL+"/breeds");
    },
    GetImage : function(animal_internal_id,image_id){
        return BASE_API_URL+"/view_image?animal_internal_id="+animal_internal_id+"&image_id="+image_id;
    },
    FindSimilarImagesByIds : async function(ids){
        return await axios.get(BASE_EMBEDDING_URL+"/find_similar_from_ids?ids="+ids);
    },
    FindSimilarImagesByImage : async function(formData){
        return await axios.post(BASE_EMBEDDING_URL+'/find_similar_from_image', formData, {
            headers: {
                'Content-Type': 'multipart/form-data'
            }
        })
    },
    ChatWithDog : async function(chat){
        return await axios.post(BASE_MODEL_URL+"/chat_with_dog",chat);
    }
}

export default DataServices;