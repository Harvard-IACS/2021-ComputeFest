import React from 'react';
import { withStyles } from '@material-ui/core/styles';

const styles = theme => ({
    grow: {
        flexGrow: 1,
    },
    root: {
        height: "100%",
        backgroundColor: "#e6ffea",
    },
});

const Content = props => {
    const classes = props.classes;

    const children = props.children;

    console.log("================================== Content ======================================");

    return (
        <div className={classes.root}>
            {children}
        </div>
    );
}

export default withStyles( styles )( Content );