import React, { Suspense, useState } from "react";
import { defer } from "react-router-dom";
import api from "../../../utils/auth/axiosInstance";
import { Await, useLoaderData } from "react-router-dom";
import Spinner from "../../common/Spinner";
import {jwtDecode} from 'jwt-decode'
import { Box, Button, Typography, Card, CardContent, CardActions, IconButton, InputLabel, TextField, Alert } from "@mui/material";
import { Table, TableContainer, TableBody, TableHead, TableRow, TableCell } from "@mui/material";
import Grid from '@mui/material/Grid';
import GradingIcon from '@mui/icons-material/Grading';
import Paper from "@mui/material/Paper";
import CKEditorField from "../../common/CKEditorField";
import { FormControl, FormControlLabel, Radio, RadioGroup, FormLabel } from '@mui/material';
import DeleteIcon from '@mui/icons-material/Delete';
import Modal from '@mui/material/Modal';
import EditIcon from '@mui/icons-material/Edit';
import UploadFileIcon from '@mui/icons-material/UploadFile';
import SchoolIcon from '@mui/icons-material/School';
import StickyAppBar from "../../common/StickyAppBar";
import PropTypes from 'prop-types';



const modalStyle = {
    position: "absolute",
    top: "50%",
    left: "50%",
    transform: "translate(-50%, -50%)",
    maxHeight: "90vh",
    // width: { xs: "20rem", sm: "70rem", md: "70rem", lg: "70rem", xl: "70rem" },
    bgcolor: "background.paper",
    boxShadow: 24,
    borderRadius: "1rem",
    overflow: "auto",
    p: 4,
    width: 800,
  };
function StudentProfilePage(){


    

    const { initial_data } = useLoaderData();
    return (
        <>
            
            <Suspense fallback={Spinner}>
                <Await resolve={ initial_data }>
                    { (resolvedData) => <StudentProfileData initial_data={resolvedData} /> }
                </Await>
            </Suspense>
        </>
    )
}

export default StudentProfilePage;

const StudentProfileData = ( {initial_data}) =>{
    const [open, setOpen] = useState(false);
    const [projects, setProjects] = useState([]);
    const [url, setUrl] = useState('');
    const [description, setDescription] = useState('');
    const [editIndex, setEditIndex] = useState(null);
    const [resumeFileName, setResumeFileName] = useState('');
    const [ formData, setFormData ] = useState({});

    const handleFileChange = (e) => {
        if(e.target.files.length > 0){
            setResumeFileName(e.target.files[0].name);
            setFormData({
                ...formData,
                'resume': e.target.files[0]
            });
        }
    }

    const handleFormUpdate = (e) => {
        const { name, value } = e.target;
        setFormData({
            ...formData,
            [name]: value
        })
    }
    
    const handleOpen = (index = null) => {
        setOpen(true)
    };
    const handleEdit = (index = null) => {
        console.log("handleOpen called with index:", index); // Debug log
        if( index != null ){
            // alert('index is not null')
            console.log("index");
            console.log(index);
            setUrl(projects[index].url);
            setDescription(projects[index].description);
            setEditIndex(index);
        }
        setOpen(true)
    };
    const handleClose = () => {
        setOpen(false);
        setUrl('');
        setDescription('');
        setEditIndex(null);
    };

    const handleAddProject = ( ) => {
        console.log("editIndex", editIndex);
        if(editIndex !== null){
            console.log("Edit index is not null", editIndex);
            const updatedProjects = [...projects];
            console.log("url", url);
            console.log("description", description);
            updatedProjects[editIndex] = { url, description};
            console.log("updatedProjects");
            console.log(updatedProjects);
            setProjects(updatedProjects);
        }else{
            console.log("Edit index is  null", editIndex)
            setProjects([...projects, {url, description}]);
        }
      handleClose()  ;
    };

    const handleDeleteProject = (index) => {
        setProjects(projects.filter((_,i) => i !== index ));
    }

    const handleUpdateProfile = () => {
        console.log("Handling ******* upate");
        try {
            
            const token = localStorage.getItem('access');
            // await sleep(2000);
            if(!token){
                throw new Error('Not authorised')
            }
            const decodedToken = jwtDecode(token);
            const user_id = decodedToken.user_id;
            const endpoint = `api/students/${user_id}`;
            const headers = {
                'Content-Type': 'multipart/form-data'
            }
            console.log("formData *****************************");
            console.log(formData);
            const response = api.patch(endpoint, formData, { headers });
            console.log("Updated successfully");
        } catch (error) {
            console.log("Updated failed");
            console.log(error);
        }
    }
    const buttonsData = [
        // {
        //     "color": "warning",
        //     "onClickHandler": () => { console.log("handleDraft")},
        //     "btnText": "Save as Drafts"
        // },
        {
            "color": "success",
            "onClickHandler": handleUpdateProfile,
            "btnText": "Update Profile"
        }
    ];

    // Student Profile Data
    const fullname = `${initial_data.first_name} ${initial_data.last_name}`
    const {scores} = initial_data;
    const hasScores = scores && Object.keys(scores).length > 0;
    console.log("scores");
    console.log(typeof scores);
    console.log(scores);
    console.log(scores.length);
    Object.entries(scores).map(([course, details]) => {
        console.log(course);
        console.log(details.grade);
        console.log(details.timemodified);
       
    })
    
    
    return(
        <>
            <StickyAppBar appBarTitle="Student Profile" cancelBtnText="Back" cancelLink="/auth/employer/jobs" buttonsData={buttonsData} />
            <Grid container spacing={2} component="form">
                <Grid md={6} item>
                    <TextField
                        disabled
                        fullWidth
                        label="Name"
                        id="name"
                        size="small"
                        value={fullname}
                    />
                </Grid>
                <Grid md={6} item>
                    <TextField
                            disabled
                            fullWidth
                            label="Email"
                            id="email"
                            size="small"
                            value={initial_data.email}
                        />
                </Grid>
            </Grid>
            <Grid container spacing={2} mt={2}>
                <Grid item md={12}>
                    <Alert icon={<GradingIcon/>} severity="success">
                        Spoken Tutorial Test Scores
                    </Alert>
                </Grid>
                {/* { hasScores ? (<p>Scores available</p>):( <p>Scores not available</p>) } */}
                <Grid item md={12}>
                    <TableContainer  sx={{ minWidth: 650 }} component={Paper}>
                        <Table  sx={{ width: '100%' }}>
                            <TableHead >
                                <TableRow>
                                    <TableCell><b>Course</b></TableCell>
                                    <TableCell><b>Grade</b></TableCell>
                                    <TableCell><b>Test Date</b></TableCell>
                                </TableRow>
                            </TableHead>
                            <TableBody>
                            {
                                Object.entries(scores).map(([course, details]) => (
                                    
                                        <TableRow key={course}>
                                            <TableCell>{course}</TableCell>
                                            <TableCell>{details.grade}</TableCell>
                                            <TableCell>{details.timemodified}</TableCell>
                                        </TableRow>
                                ))
                            }
                            </TableBody>
                        </Table>
                    </TableContainer>
                </Grid>
            </Grid>
            <Grid container spacing={2} mt={2}>
                <Grid md={6} item>
                    <TextField
                        disabled
                        fullWidth
                        label="Phone"
                        id="phone"
                        size="small"
                        value={initial_data.phone || ''}
                    />
                </Grid>
                <Grid md={6} item>
                    <TextField
                            fullWidth
                            label="Alternate Email"
                            id="alternate_email"
                            name="alternate_email"
                            size="small"
                            type="email"
                            value={formData.alternate_email}
                            onChange={handleFormUpdate}
                        />
                </Grid>
                <Grid md={12} item>
                    <TextField
                            fullWidth
                            label="Address"
                            id="address"
                            size="small"
                            type="email"
                            multiline
                            rows={2}
                            value={initial_data.address || ''}
                        />
                </Grid>
                <Grid md={12} item>
                    <InputLabel>About Yourself</InputLabel>
                    <CKEditorField
                    label="About Yourself" id="about"
                    value={initial_data.about || ''}
                    />
                </Grid>
                <Grid item md={6}>
                    
                    <Box border={1} borderRadius={2} padding={2} sx={{ borderColor: 'grey.500' }}>
                        <FormControl component="fieldset">
                            <FormLabel component="legend">If offered a job, will you be able to join immediately?</FormLabel>
                            <RadioGroup aria-label="join-immediately" name="joinImmediately"
                                value={initial_data.joining_immediate ? 'yes' : 'no'}>
                                <FormControlLabel 
                                control={<Radio/>} label="yes"></FormControlLabel>
                                <FormControlLabel 
                                value="no" 
                                control={<Radio/>} label="no"></FormControlLabel>
                            </RadioGroup>
                        </FormControl>
                    </Box>
                    
                    {/* <FormControl component="fieldset">
                        <FormLabel component="legend">Are you willing to relocate based on job requirement?</FormLabel>
                        <FormGroup>
                            <FormControlLabel control={<Checkbox name="relocateNo" />} label="No" />
                            <FormControlLabel control={<Checkbox name="relocateState" />} label="Within the state" />
                            <FormControlLabel control={<Checkbox name="relocateIndia" />} label="Anywhere in India" />
                            <FormControlLabel control={<Checkbox name="relocateOverseas" />} label="Overseas" />
                            </FormGroup>
                    </FormControl> */}
                </Grid>
                <Grid item md={6}>
                <Box border={1} borderRadius={2} padding={2} sx={{ borderColor: 'grey.500' }}>
                    <FormControl component="fieldset">
                        <FormLabel component="legend">Are you interested for an internship?</FormLabel>
                        <RadioGroup aria-label="internship" name="internship"
                            value={initial_data.avail_for_intern ? 'yes' : 'no'}>
                            <FormControlLabel value="yes" control={<Radio/>} label="yes"></FormControlLabel>
                            <FormControlLabel value="no" control={<Radio/>} label="no"></FormControlLabel>
                        </RadioGroup>
                    </FormControl>
                </Box>
                
                </Grid>
                <Grid item >
                    <Alert icon={<GradingIcon/>} severity="success">Projects</Alert>
                        <Box mt={2}><Button variant="contained" color="primary" onClick={handleOpen} >Add Project</Button></Box>
                    <Box mt={2}>
        {projects.map((project, index) => (
          <Card key={index} sx={{ mb: 2 }}>
            <CardContent>
              <Typography variant="h6" component="div">
                Project {index + 1}
              </Typography>
              <Typography variant="body2" color="textSecondary">
                <strong>URL:</strong> {project.url}
              </Typography>
              <Typography variant="body2" color="textSecondary">
                <strong>Description:</strong> {project.description}
              </Typography>
            </CardContent>
            <CardActions>
              <IconButton color="primary" onClick={() => handleEdit(index)}>
                <EditIcon />
              </IconButton>
              <IconButton color="secondary" onClick={() => handleDeleteProject(index)}>
                <DeleteIcon />
              </IconButton>
            </CardActions>
          </Card>
        ))}
      </Box>
      <Modal
        open={open}
        onClose={handleClose}
        aria-labelledby="modal-title"
        aria-describedby="modal-description"
      >
        <Box
          sx={{
            position: 'absolute',
            top: '50%',
            left: '50%',
            transform: 'translate(-50%, -50%)',
            width: 800,
            bgcolor: 'background.paper', // Ensure the background is set to paper color (white)
            border: '2px solid #000',
            boxShadow: 24,
            p: 4,
          }}
        >
          <Typography id="modal-title" variant="h6" component="h2">
            {editIndex !== null ? 'Edit Project' : 'Add a New Project'}
          </Typography>
          <TextField
            fullWidth
            label="URL"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            margin="normal"
          />
          <TextField
            fullWidth
            label="Project Description"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            margin="normal"
            multiline
            rows={8}
          />
          <Button variant="contained" color="primary" onClick={handleAddProject} sx={{ mt: 2 }}>
            {editIndex !== null ? 'Save Changes' : 'Add Project'}
          </Button>
        </Box>
      </Modal>
                </Grid>
                <Grid item md={12}>
                <InputLabel>Certifications</InputLabel>
                    <CKEditorField
                    label="Certifications" id="certifications"
                    value={initial_data.certifications || ''}
                    />
                </Grid>
                <Grid item md={6}>
                    <TextField
                        fullWidth
                        label="LinkedIn"
                        value={initial_data.linkedin}
                    />
                </Grid>
                <Grid item md={6}>
                    <TextField
                        fullWidth
                        label="Github"
                        value={initial_data.github}
                    />
                </Grid>
                <Grid item md={12}>
                   <Box>
                        <Typography>Resume Upload</Typography>
                        <input
                        accept=".pdf,.doc,.docx"
                        style={{ display: 'none' }}
                        id="raised-button-file"
                        type="file"
                        onChange={handleFileChange}
                        />
                        <label htmlFor="raised-button-file">
                        <Button variant="outlined" color="primary" component="span" startIcon={<UploadFileIcon />} size="small">
                            {/* {resumeFileName || 'Upload Resume'} */}
                            { resumeFileName || 'Upload Resume'}
                        </Button>
                        </label>
                   </Box>
                </Grid>
                <Grid item md={12}>
                    <Alert icon={<SchoolIcon/>} severity="success">Education</Alert>
                </Grid>
                <Grid item md={6}>
                    <TextField
                        fullWidth disabled
                        label="Institute Name"
                        value={initial_data.academic}

                    />
                </Grid>
                <Grid item md={6}>
                    <TextField
                        fullWidth disabled
                        label="Institute Type"
                        value={initial_data.insti_type}
                    />
                </Grid>
                {/* <Grid item md={6}>
                    <TextField
                        fullWidth disabled
                        label="University Name"
                        
                    />
                </Grid> */}
                <Grid item md={6}>
                    <TextField
                        fullWidth disabled
                        label="Degree"
                        value={initial_data.department}                        
                    />
                </Grid>
                <Grid item md={4}>
                    <TextField
                        fullWidth disabled
                        label="Admission Year"
                        value={initial_data.year}
                        
                        
                    />
                </Grid>
                <Grid item md={4}>
                    <TextField
                        fullWidth disabled
                        label="State"
                        value={initial_data.state}
                        
                    />
                </Grid>
                <Grid item md={4}>
                    <TextField
                        fullWidth disabled
                        label="City"
                        value={initial_data.city}
                        
                    />
                </Grid>
            </Grid>
        </>
    )
}

StudentProfileData.propTypes = {
    initial_data: PropTypes.object.isRequired
}

export async function loader(){
    try {
        // get the user id from local storage
        const token = localStorage.getItem('access');
        // await sleep(2000);
        if(!token){
            throw new Error('Not authorised')
        }
        const decodedToken = jwtDecode(token);
        const user_id = decodedToken.user_id;
        const endpoint = `api/student-initial-data/${user_id}`;
        const response = await api.get(endpoint);
        console.log(response.data);
        return defer({ initial_data: response.data });
    } catch (error) {
        // throw error;
        console.log("error");
    }
}

