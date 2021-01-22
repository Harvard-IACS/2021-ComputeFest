import React, {useEffect, useState} from 'react';
import {useDropzone} from 'react-dropzone';
import { withStyles } from '@material-ui/core/styles';
import Icon from "@material-ui/core/Icon";
import IconButton from "@material-ui/core/IconButton";

const styles = {
    root: {

    },
};

const thumbsContainer = {
    display: 'flex',
    flexDirection: 'row',
    flexWrap: 'wrap',
    marginTop: 1
};

const thumb = {
    display: 'inline-flex',
    borderRadius: 2,
    border: '1px solid #eaeaea',
    marginBottom: 8,
    marginRight: 8,
    width: 400,
    height: 250,
    padding: 4,
    boxSizing: 'border-box'
};

const thumbInner = {
    display: 'flex',
    minWidth: 0,
    // overflow: 'hidden'
};

const img = {
    display: 'block',
    width: 'auto',
    height: '100%'
};

const ImageUpload = ( props ) => {

    console.log("================================== ImageUpload ======================================");
    console.log(props);

    const [files, setFiles] = useState([]);
    const {getRootProps, getInputProps} = useDropzone({
        accept: 'image/*',
        onDrop: acceptedFiles => {
            setFiles(acceptedFiles.map(file => Object.assign(file, {
                preview: URL.createObjectURL(file)
            })));

            props.onChange(acceptedFiles);
        }
    });

    const remove = (idx) => {
        console.log(idx);
        setFiles([]);
        // const newFiles = [...files];     // make a var for the new array
        // acceptedFiles.splice(file, 1);        // remove the file from the array
    };
    const thumbs = files.map((file, i) => (
        <div style={thumb} key={file.name}>
            <div style={thumbInner}>
                <img
                    src={file.preview}
                    style={img}
                />
                <IconButton aria-label="clear" color="default" onClick={() => remove(i)}>
                    <Icon fontSize="large">cancel</Icon>
                </IconButton>
            </div>
        </div>
    ));

    useEffect(() => () => {
        // Make sure to revoke the data uris to avoid memory leaks
        files.forEach(file => URL.revokeObjectURL(file.preview));
    }, [files]);

    return (
        <section className="container">
            <div {...getRootProps({className: 'dropzone'})} style={{
                flex: 1,
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
                paddingLeft: 15,
                paddingRight: 15,
                paddingTop:3,
                paddingBottom:3,
                borderWidth: 1,
                borderRadius: 2,
                borderColor: "#bebebe",
                borderStyle: "solid",
                backgroundColor: "#ffffff",
                color: "#7e7e7e",
                outline: "none",
                transition: "border .24s ease-in-out",
                cursor: "pointer",
            }}>
                <input {...getInputProps()} />
                <p style={{cursor: "pointer"}}>Upload to find similar dogs</p>
            </div>
            <aside style={thumbsContainer}>
                {thumbs}
            </aside>
        </section>
    );
}

export default withStyles( styles )( ImageUpload );