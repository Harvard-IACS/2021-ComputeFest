import React, {useEffect, useRef, useState} from 'react';
import { withStyles } from '@material-ui/core/styles';
import Container from '@material-ui/core/Container';
import Grid from '@material-ui/core/Grid';
import GridList from '@material-ui/core/GridList';
import GridListTile from '@material-ui/core/GridListTile';
import Paper from '@material-ui/core/Paper';
import FormControl from '@material-ui/core/FormControl';
import Select from '@material-ui/core/Select';
import InputLabel from '@material-ui/core/InputLabel';
import MenuItem from '@material-ui/core/MenuItem';
import TextField from '@material-ui/core/TextField';
import Checkbox from '@material-ui/core/Checkbox';

import Typography from '@material-ui/core/Typography';
import Card from '@material-ui/core/Card';
import CardHeader from '@material-ui/core/CardHeader';
import CardMedia from '@material-ui/core/CardMedia';
import CardContent from '@material-ui/core/CardContent';
import CardActions from '@material-ui/core/CardActions';
import Icon from "@material-ui/core/Icon";
import IconButton from '@material-ui/core/IconButton';
import Button from '@material-ui/core/Button';

import { Widget,toggleWidget,dropMessages,addResponseMessage } from 'react-chat-widget';

import ImageUpload from './ImageUpload';
import DataServices from "../../services/DataServices";

import 'react-chat-widget/lib/styles.css';
import './style.css';


const styles = theme => ({
    root: {
        flexGrow: 1,

    },
    grow: {
        flexGrow: 1,
    },
    main: {
        backgroundColor: "#e6ffea",
        paddingLeft: theme.spacing(3),
        paddingRight: theme.spacing(3),
        paddingBottom: theme.spacing(2),
        paddingTop: 15,
        zIndex: theme.zIndex.drawer + 1,
    },
    paper: {
        padding: theme.spacing(2),
        color: theme.palette.text.secondary,
        width: '100%',
    },
    formControl: {
        // margin: theme.spacing(3),
        marginLeft: 24,
        marginRight:24,
        minWidth: 100,
    },
    media:{
        height: 0,
        paddingTop: '95%', // '56.25%' 16:9
    },
    gridList: {
        height: 650,

    },
    thumbnailImage: {
        opacity: 1.0,
        '&:hover': {
            opacity: 1
        }
    },
    predictionImage:{
        height: 0,
        paddingTop: '100%',
        opacity: 1.0,
    },
    progressBar: {
        position: "absolute",
        top: "300px",
        left: "48%",
        color: "#ffffff"
    },
    card: {
        margin: 5,
        // height: 250,
        // width: '23%',
    }
});

const Home = ( props ) => {
    const {classes} = props;
    const { history } = props;

    console.log("================================== Home ======================================");

    // Search Filters
    const [filterBreed, setFilterBreed] = useState('');
    const [filterAgeGT, setAgeGT] = useState('');
    const [filterAgeLT, setAgeLT] = useState('');
    const [filterSimilar, setFilterSimilar] = useState([]);
    const [chatDog, setChatDog] = useState(null);
    const [chatHistory, setChatHistory] = useState([]);

    // Store the list of breeds
    const [breeds, setBreeds] = useState([]);
    const loadBreeds = () => {
        DataServices.GetBreeds()
            .then(function (response) {
                console.log(response.data);
                setBreeds(response.data);
            })
    }

    // Store the list of dogs
    const [dogs, setDogs] = useState([]);
    const loadDogs = () => {
        DataServices.GetDogs(filterBreed)
            .then(function (response) {
                console.log(response.data);
                setDogs(response.data);
            })
    }

    // Load initial datasets
    useEffect(() => {
        loadBreeds();
        loadDogs();
    }, []);

    // Reload based on filter changes
    useEffect(() => {
        closeChatWindow();
        loadDogs();
    }, [filterBreed]);

    // Handle events
    const handleBreedChange = (event) => {
        setFilterBreed(event.target.value);
    };
    const handleAgeGTChange = (event) => {
        setAgeGT(event.target.value);
    };
    const handleAgeLTChange = (event) => {
        setAgeLT(event.target.value);
    };
    const handleSelectDog = (event, ischecked) => {
        var selectedDogs = [...filterSimilar];
        console.log(event.target.value, ischecked);
        if(ischecked){
            if(!selectedDogs.includes(event.target.value)){
                selectedDogs.push(event.target.value)
            }
        }else{
            var idx = selectedDogs.findIndex(function (element) {
                return element == event.target.value;
            });
            if(idx >= 0){
                selectedDogs.splice(idx, 1)
            }
        }
        setFilterSimilar(selectedDogs);
        console.log(selectedDogs)
    }
    const handleImageUpload = (files) => {
        console.log(files);
        var formData = new FormData();
        formData.append("file", files[0]);
        formData.append("filename", files[0]["name"]);

        DataServices.FindSimilarImagesByImage(formData)
            .then(function (response) {
                console.log(response.data);
                setDogs(response.data);
            })
    };
    const displayFindSimilar = () =>{
        console.log(filterSimilar.length)
        if(filterSimilar.length > 0){
            return true;
        }else{
            return false;
        }
    }
    const findSimilarBasedOnSelections = () => {
        console.log(filterSimilar)
        let ids = filterSimilar.join(",")
        ids = ids.replaceAll('"','');

        DataServices.FindSimilarImagesByIds(ids)
            .then(function (response) {
                console.log(response.data);
                setDogs(response.data);
            })
    }

    // Chat
    const handleDogChat = (dog) => {
        dropMessages();
        console.log(dog);
        setChatDog(dog);
        if (isChatWidgetOpen()){
            toggleWidget();
        }

        addResponseMessage("Woof Woof!")
    }
    const displayChatWindow = () =>{
        if(!chatDog){
            return false;
        }else{
            return true;
        }
    }
    const closeChatWindow = () =>{
        dropMessages();
        if (!isChatWidgetOpen()){
            toggleWidget();
        }
        setChatDog(null);
    }
    const isChatWidgetOpen = () => {
        if(!chatDog){
            return false;
        }else{
            return true;
        }
    }
    const isDogHighlited = (dog) => {
        let style = {};
        let selectedStyle = {
            border:"7px solid #31a354"
        }
        if(chatDog && (dog.AnimalInternalID == chatDog.AnimalInternalID)){
            style = selectedStyle
        }
        return style;
    }
    const handleChatWithDog = (message) => {
        var history = [...chatHistory];
        console.log(message);
        let chat = {
            "dog":chatDog,
            "history": history,
            "input_message":message
        }
        // Chat with backend API
        DataServices.ChatWithDog(chat)
            .then(function (response) {
                console.log(response.data);
                let chat_response = response.data;
                addResponseMessage(chat_response["response_message"]);
                history.push(message);
                history.push(chat_response["response_message"]);

                // if(history.length > 5){
                //
                // }
                history = history.slice(Math.max(history.length - 5, 0))

                setChatHistory(history);
                console.log(history)
            })
    }
    const clearFilters = () => {
        setFilterBreed('');
        setFilterSimilar([]);
        setChatDog(null);
        closeChatWindow();
        loadDogs();
    }


    return (
        <div className={classes.root}>
            <main className={classes.main}>
                <Container fixed>
                    <Grid container spacing={3}>
                        <Paper className={classes.paper}>
                            <FormControl className={classes.formControl}>
                                <InputLabel>Breed:</InputLabel>
                                <Select value={filterBreed} onChange={handleBreedChange}>
                                    <MenuItem key={-1} value=''>-Select-</MenuItem>
                                    {breeds.map((breed,i) => (
                                        <MenuItem key={i} value={breed}>{breed}</MenuItem>
                                    ))}
                                </Select>
                            </FormControl>
                            <FormControl className={classes.formControl}>
                                <TextField
                                    label="Age &#62; (years)"
                                    type="number"
                                    InputLabelProps={{
                                        shrink: true,
                                    }}
                                    variant="outlined"
                                    value={filterAgeGT}
                                    onChange={handleAgeGTChange}
                                />
                            </FormControl>
                            <FormControl className={classes.formControl}>
                                <TextField
                                    label="Age &#60; (years)"
                                    type="number"
                                    InputLabelProps={{
                                        shrink: true,
                                    }}
                                    variant="outlined"
                                    value={filterAgeLT}
                                    onChange={handleAgeLTChange}
                                />
                            </FormControl>
                            <FormControl className={classes.formControl}>
                                <ImageUpload onChange={handleImageUpload}></ImageUpload>
                            </FormControl>
                            {displayFindSimilar() && (
                                <FormControl className={classes.formControl}>
                                    <div style={{
                                        flex: 1,
                                        display: "flex",
                                        flexDirection: "column",
                                        alignItems: "center",
                                        paddingLeft: 15,
                                        paddingRight: 15,
                                        paddingTop:18,
                                        paddingBottom:18,
                                        borderWidth: 1,
                                        borderRadius: 2,
                                        borderColor: "#bebebe",
                                        borderStyle: "solid",
                                        backgroundColor: "#ffffff",
                                        color: "#7e7e7e",
                                        outline: "none",
                                        transition: "border .24s ease-in-out",
                                        cursor: "pointer",
                                    }}
                                    onClick={findSimilarBasedOnSelections}
                                    >
                                        Find similar dogs to selection(s)
                                    </div>
                                </FormControl>
                            )}
                            <IconButton aria-label="clear" color="default" onClick={clearFilters}>
                                <Icon fontSize="large">delete</Icon>
                            </IconButton>
                        </Paper>
                    </Grid>
                </Container>
                <div>&nbsp;</div>
                <Container fixed style={{paddingLeft:10,paddingRight:10}}>
                    <Grid container spacing={0}>
                        {dogs.map((dog) => (
                            <Grid key={dog.ImageID} item xs={4}>
                                <Card className={classes.card} style={isDogHighlited(dog)}>
                                    <CardMedia
                                        className={classes.media}
                                        image={DataServices.GetImage(dog.AnimalInternalID,dog.ImageID)}
                                        title={dog.AnimalName}
                                    />
                                    <CardHeader
                                        title={dog.AnimalName}
                                        subheader={dog.AnimalBreed+', '+dog.Age+' year(s)'}
                                    />
                                    <CardActions disableSpacing>
                                        <Checkbox
                                            color="primary"
                                            value={dog.ImageID}
                                            onChange={handleSelectDog}
                                        />
                                        <IconButton aria-label="share" color="primary" onClick={()=>handleDogChat(dog)}>
                                            <Icon fontSize="large">chat_bubble</Icon>
                                        </IconButton>
                                    </CardActions>
                                </Card>
                            </Grid>
                        ))}
                    </Grid>
                </Container>
                {displayChatWindow() && (
                    <div>
                        <Widget
                            title={'🐶 I am '+chatDog.AnimalName}
                            subtitle={'Ask me anything'}
                            handleNewUserMessage={handleChatWithDog}
                        />
                    </div>
                )}
            </main>
        </div>
    );
};

export default withStyles( styles )( Home );