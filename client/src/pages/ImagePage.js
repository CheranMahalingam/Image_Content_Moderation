import React, {useState} from "react";
import AppBar from '@material-ui/core/AppBar';
import Tabs from '@material-ui/core/Tabs';
import Tab from '@material-ui/core/Tab';
import Typography from '@material-ui/core/Typography';
import FileUpload from "../components/FileUpload/FileUpload";
import PublicGallery from "../components/ViewImages/PublicGallery";
import PrivateImageRepository from "../components/ViewImages/PrivateImageRepository";

function ImagePage() {
    const [tab, setTab] = useState(0);

    const handleTabChange = (_, newTab) => {
        setTab(newTab);
    }

    return (
        <>
            <AppBar position="static">
                <Tabs value={tab} onChange={handleTabChange}>
                    <Tab label="Image Upload" />
                    <Tab label="View Your Images" />
                    <Tab label="Public Gallery" />
                </Tabs>
            </AppBar>
            {tab === 0 ? <FileUpload /> : null}
            {tab === 1 ? <PrivateImageRepository /> : null}
            {tab === 2 ? <PublicGallery /> : null}
        </>
    )
}

export default ImagePage;