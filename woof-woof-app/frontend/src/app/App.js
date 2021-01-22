import React from 'react'
import { BrowserRouter as Router } from 'react-router-dom';
import CssBaseline from '@material-ui/core/CssBaseline';
import AppRoutes from "./AppRoutes";
import { ThemeProvider } from '@material-ui/core/styles';
import Theme from "./Theme";
import Content from "../common/layout/Content";
import Header from "../common/layout/Header";

import DataServices from '../services/DataServices';

const App = (props) => {

    console.log("================================== App ======================================");

    DataServices.Init();

    // Build App
    let view = (
        <React.Fragment>
            <CssBaseline />
            <ThemeProvider theme={Theme}>
                <Router basename="/">
                    <Header></Header>
                    <Content>
                        <AppRoutes />
                    </Content>
                </Router>
            </ThemeProvider>
        </React.Fragment>
    )

    // Return View
    return view
}

export default App;
