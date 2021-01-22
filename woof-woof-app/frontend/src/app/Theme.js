import { createMuiTheme } from '@material-ui/core/styles';

const Theme = createMuiTheme({
    palette: {
        type: 'light',
        primary: {
            // light: will be calculated from palette.primary.main,
            main: '#31a354',
            // dark: will be calculated from palette.primary.main,
            // contrastText: will be calculated to contrast with palette.primary.main
        },
        secondary: {
            light: '#0066ff',
            main: '#1c4385',
            // dark: will be calculated from palette.secondary.main,
            contrastText: '#ffffff',
        },
        // error: will use the default color

    },
    typography: {
        useNextVariants: true,
        h6: {
            color: "#31a354",
            fontSize: "1.1rem",
            fontFamily: "Roboto, Helvetica, Arial, sans-serif",
            fontWeight:800
        },
        h5: {
            color: "#31a354",
            fontSize: "1.1rem",
            fontFamily: "Roboto, Helvetica, Arial, sans-serif",
            fontWeight:800
        },
    },
});

export default Theme;