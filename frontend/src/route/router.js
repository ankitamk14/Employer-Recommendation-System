import { createBrowserRouter } from "react-router-dom";

import Layout from "../pages/Layout";

//essentials
import Error from "../pages/Error";
import ProtectedRoute from "../components/common/protectedRoute";
import UnderDevelopmentInfo from "../components/common/underDevelopment";

//unauth common
import Homepage, { loader as HomePageLoader } from "../pages/Homepage";
import ViewAllEvents, {
  loader as ViewAllEventsLoader,
} from "../components/eventsSection/viewAllEvents";
import ViewAllCompanies, {
  loader as ViewAllCompaniesLoader,
} from "../components/companiesSection/viewallCompanies";
import ViewAllTestimonials, {
  loader as ViewAllTestimonialsLoader,
} from "../components/Testimonials/viewAllTestimonials";
import ViewAllGallery from "../components/gallerySection/viewAllGallery";
import AddJobForm, { loader as addJobLoader } from "../components/company/company-job-profile/AddJob"; 
//login /reset
import LoginForm, {
  action as LoginAction,
} from "../components/login/loginForm";

import NewPasswordInput, {
  action as NewPasswordInputAction,
} from "../components/login/ForgotPassword/NewPasswordInput";

//student
import StudentLayout, {
  action as StudentLogoutAction,
} from "../pages/StudentLayout";
import StudentProfile from "../components/student/student-profile/studentProfile";
import RegisterCompany, { loader as registerCompanyLoader } from "../components/company/company-registration/RegisterCompany";

//company
import EmployerLayout, {
  action as EmployerLogoutAction,
} from "../pages/EmployerLayout";
import CompanyJobProfile, {
  loader as jobListLoader,
} from "../components/company/company-job-profile/companyJobProfile";
// import AddNewJob, {
//   loader as initialFormDataLoader,
// } from "../components/company/company-job-profile/AddNewJobDailog/AddNewJob";
import AddNewJob from "../components/company/company-job-profile/AddNewJobDailog/AddNewJob";
// import EditJobDialog, {
//   loader as EditJobInitialDataLoader,
// } from "../components/company/company-job-profile/EditJobDailog/EditJobDialog";
// import AddNewCompany, {
//   loader as initialCompanyFormDatLoader,
// } from "../components/company/company-registration/AddNewCompany";
import EmployerDashboard, {loader as empDashboardLoader} from "../components/company/dashboard/EmployerDashboard";
import UpdateJob, { loader as JobDataLoader} from "../components/company/company-job-profile/UpdateJob";
//manager
import ManagerLayout, {
  action as ManagerLogoutAction,
} from "../pages/ManagerLayout";
import FossFilter from "../components/admin/foss-filter/FossFilter";
import CompanyRegistration, { loader as Cloader, action as Caction} from "../pages/CompanyRegistration";
import CompanyUserProfile, {loader as companyUserProfileLoader} from "../components/company/company-job-profile/Profile";
// import StudentProfileData from "../components/student/student-profile/studentProfileData";
import StudentProfilePage, { loader as studentProfileLoader } from "../components/student/student-profile/studentProfileData";

const router = createBrowserRouter([
  {
    //common without auth routes
    path: "/",
    element: <Layout />,
    errorElement: <Error />,
    children: [
      { path: "/company/registration", element: <CompanyRegistration />, loader: Cloader, action: Caction },
      { path: "/", element: <Homepage />, loader: HomePageLoader },
      {
        path: "/events/view-all/:pageNum",
        element: <ViewAllEvents />,
        loader: ViewAllEventsLoader,
      },
      {
        path: "/companies/view-all/:pageNum",
        element: <ViewAllCompanies />,
        loader: ViewAllCompaniesLoader,
      },
      { path: "/gallery/view-all", element: <ViewAllGallery /> },
      {
        path: "/testimonials/view-all/:pageNum",
        element: <ViewAllTestimonials />,
        loader: ViewAllTestimonialsLoader,
      },
      { path: "/foss-filter", element: <FossFilter /> },
      {
        path: "/company-registration",
        // element: <AddNewCompany />,
        element: <RegisterCompany/>,
        loader: registerCompanyLoader,
      },
      {
        path: "/login",
        element: (
          <ProtectedRoute accessBy={"unauth"} roleAllowed={null}>
            <LoginForm />
          </ProtectedRoute>
        ),
        action: LoginAction,
      },
      {
        path: "/reset-password/:password_token",
        element: <NewPasswordInput />,
        action: NewPasswordInputAction,
      },
    ],
  },

  {
    //student related auth routes
    path: "/auth/student",
    element: (
      <ProtectedRoute accessBy={"auth"} roleAllowed={["STUDENT"]}>
        <StudentLayout />
      </ProtectedRoute>
    ),
    action: StudentLogoutAction,
    children: [
      { path: "dashboard", element: <UnderDevelopmentInfo /> },
      { path: "profile", element: <StudentProfile /> },
      { path: "student-profile", element: <StudentProfilePage />, 
        loader: studentProfileLoader
       },

      
      { path: "jobs", element: <UnderDevelopmentInfo /> },
    ],
  },

  {
    //manager related auth routes
    path: "/auth/manager/dashboard",
    element: (
      <ProtectedRoute accessBy={"auth"} roleAllowed={["MANAGER"]}>
        <ManagerLayout />
      </ProtectedRoute>
    ),
    action: ManagerLogoutAction,
    children: [{ path: "", element: <UnderDevelopmentInfo /> }],
  },

  {
    //employer related auth routes
    path: "/auth/employer",
    element: (
      <ProtectedRoute accessBy={"auth"} roleAllowed={["EMPLOYER"]}>
        <EmployerLayout />
      </ProtectedRoute>
    ),
    action: EmployerLogoutAction,
    children: [
      { path: "dashboard", element: <EmployerDashboard />, loader: empDashboardLoader },
      { path: "jobs", element: <CompanyJobProfile />, loader: jobListLoader },
      // { path: "profile", element: <UnderDevelopmentInfo /> },
      { path: "profile", 
      element: <CompanyUserProfile/> ,
      loader: companyUserProfileLoader},
    ],
  },
  {
    path: "/auth/employer/jobs/addNewJob",
    element: (
      <ProtectedRoute accessBy={"auth"} roleAllowed={"EMPLOYER"}>
        <AddNewJob />
      </ProtectedRoute>
    ),
    // loader: initialFormDataLoader,
  },
  {
    path: "/auth/employer/jobs/add",
    element: (
      <ProtectedRoute accessBy={"auth"} roleAllowed={"EMPLOYER"}>
        <AddJobForm />
      </ProtectedRoute>
    ),
    loader: addJobLoader,
  },
  {
    path: "/auth/employer/jobs/editJob/:job_id",
    element: (
      <ProtectedRoute accessBy={"auth"} roleAllowed={["EMPLOYER"]}>
        {/* <EditJobDialog /> */}
        <UpdateJob/>
      </ProtectedRoute>
    ),
    loader: JobDataLoader,
    // loader: EditJobInitialDataLoader,
  },
]);

export { router };
