// // import React from "react";
// // import { BrowserRouter as Router, Navigate, Route, Routes } from "react-router-dom";

// // import Login from "./components/Login";
// // import Register from "./components/Register";
// // import Dashboard from "./components/Dashboard";
// // import Navbar from "./components/Navbar";
// // import "./App.css";

// // function PrivateRoute({ children }) {
// //   const token = localStorage.getItem("token");

// //   if (!token) {
// //     return <Navigate to="/" replace />;
// //   }

// //   return children;
// // }

// // function App() {
// //   const token = localStorage.getItem("token");

// //   return (
// //     <Router>
// //       {token && <Navbar />}
// //       <Routes>
// //         <Route path="/" element={<Navigate to={token ? "/dashboard" : "/login"} replace />} />
// //         <Route path="/login" element={<Login />} />
// //         <Route path="/register" element={<Register />} />
// //         <Route
// //           path="/dashboard"
// //           element={(
// //             <PrivateRoute>
// //               <Dashboard />
// //             </PrivateRoute>
// //           )}
// //         />
// //         <Route
// //           path="*"
// //           element={<Navigate to={token ? "/dashboard" : "/login"} replace />}
// //         />
// //       </Routes>
// //     </Router>
// //   );
// // }

// // export default App;
// import React from "react";
// import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";

// import Login from "./pages/Auth/Login";
// import Register from "./pages/Auth/Register";
// import Profile from "./pages/Profile/Profile";
// import EditProfile from "./pages/Profile/EditProfile";
// import AdminDashboard from "./pages/Admin/AdminDashboard";
// import FacultyDashboard from "./pages/Faculty/FacultyDashboard";
// import CoordinatorDashboard from "./pages/Coordinator/CoordinatorDashboard";
// import StudentDashboard from "./pages/StudentDashboard";

// import Navbar from "./components/Navbar/Navbar";

// import "./App.css";


// /* ---------- PROTECTED ROUTE ---------- */

// function PrivateRoute({ children }) {

//   const token = localStorage.getItem("token");

//   if (!token) {
//     return <Navigate to="/login" replace />;
//   }

//   return children;

// }


// /* ---------- ROLE ROUTE ---------- */

// function RoleRoute({ role, children }) {

//   const userRole = localStorage.getItem("role");

//   if (userRole !== role) {
//     return <Navigate to="/login" replace />;
//   }

//   return children;

// }


// /* ---------- APP ---------- */

// function App() {

//   const token = localStorage.getItem("token");

//   const role = localStorage.getItem("role");

//   return (

//     <Router>

//       <Routes>

//         {/* Default redirect */}

//         <Route
//           path="/"
//           element={
//             token
//               ? role === "admin"
//                 ? <Navigate to="/admin" />
//                 : role === "faculty"
//                 ? <Navigate to="/faculty" />
//                 : role === "coordinator"
//                 ? <Navigate to="/coordinator" />
//                 : <Navigate to="/student" />
//               : <Navigate to="/login" />
//           }
//         />

//         {/* Auth */}

//         <Route path="/login" element={<Login />} />

//         <Route path="/register" element={<Register />} />

//         <Route path="/profile" element={<Profile/>}/>
//         <Route path="/edit-profile" element={<EditProfile/>}/>

//         {/* Admin Dashboard */}

//         <Route
//           path="/admin"
//           element={
//             <PrivateRoute>
//               <RoleRoute role="admin">
//                 <AdminDashboard />
//               </RoleRoute>
//             </PrivateRoute>
//           }
//         />


//         {/* Faculty Dashboard */}

//         <Route
//           path="/faculty"
//           element={
//             <PrivateRoute>
//               <RoleRoute role="faculty">
//                 <FacultyDashboard />
//               </RoleRoute>
//             </PrivateRoute>
//           }
//         />


//         {/* Coordinator Dashboard */}

//         <Route
//           path="/coordinator"
//           element={
//             <PrivateRoute>
//               <RoleRoute role="coordinator">
//                 <CoordinatorDashboard />
//               </RoleRoute>
//             </PrivateRoute>
//           }
//         />


//         {/* Student Dashboard */}

//         <Route
//           path="/student"
//           element={
//             <PrivateRoute>
//               <RoleRoute role="student">
//                 <StudentDashboard />
//               </RoleRoute>
//             </PrivateRoute>
//           }
//         />


//         {/* Unknown Route */}

//         <Route
//           path="*"
//           element={
//             token
//               ? <Navigate to="/" />
//               : <Navigate to="/login" />
//           }
//         />

//       </Routes>

//     </Router>

//   );
// }

// export default App;

// import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

// import Login from "./pages/Auth/Login";
// import Register from "./pages/Auth/Register";

// import StudentDashboard from "./pages/Student/StudentDashboard";
// import BrowseNotice from "./pages/Student/BrowseNotice";

// import FacultyDashboard from "./pages/Faculty/FacultyDashboard";
// import PostNotice from "./pages/Faculty/PostNotice";

// import AdminDashboard from "./pages/Admin/AdminDashboard";
// import ManageUsers from "./pages/Admin/ManageUsers";

// import CoordinatorDashboard from "./pages/Coordinator/CoordinatorDashboard";

// import Profile from "./pages/Profile/Profile";
// import EditProfile from "./pages/Profile/EditProfile";

// function App() {
//   return (
//     <Router>
//       <Routes>

//         <Route path="/" element={<Login />} />
//         <Route path="/register" element={<Register />} />

//         <Route path="/student" element={<StudentDashboard />} />
//         <Route path="/browse" element={<BrowseNotice />} />

//         <Route path="/faculty" element={<FacultyDashboard />} />
//         <Route path="/post-notice" element={<PostNotice />} />

//         <Route path="/admin" element={<AdminDashboard />} />
//         <Route path="/manage-users" element={<ManageUsers />} />

//         <Route path="/coordinator" element={<CoordinatorDashboard />} />

//         <Route path="/profile" element={<Profile />} />
//         <Route path="/edit-profile" element={<EditProfile />} />

//       </Routes>
//     </Router>
//   );
// }

// export default App;

import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";

import Login from "./pages/Auth/Login";
import Register from "./pages/Auth/Register";

import StudentDashboard from "./pages/Student/StudentDashboard";
import BrowseNotice from "./pages/Student/BrowseNotice";

import FacultyDashboard from "./pages/Faculty/FacultyDashboard";
import PostNotice from "./pages/Faculty/PostNotice";

import AdminDashboard from "./pages/Admin/AdminDashboard";
import AdminPostNotice from "./pages/Admin/AdminPostNotice";
import ManageNotices from "./pages/Admin/ManageNotices";
import ManageUsers from "./pages/Admin/ManageUsers";

import CoordinatorDashboard from "./pages/Coordinator/CoordinatorDashboard";

import Profile from "./pages/Profile/Profile";
import EditProfile from "./pages/Profile/EditProfile";

function getNormalizedRole() {
  const role = (localStorage.getItem("role") || "").toLowerCase().trim();
  if (role === "teacher") return "faculty";
  return role;
}

function hasValidToken() {
  const token = (localStorage.getItem("token") || "").trim();
  return Boolean(token) && token !== "undefined" && token !== "null";
}

function DashboardRedirect() {
  const role = getNormalizedRole();

  if (role === "admin") return <Navigate to="/admin" replace />;
  if (role === "faculty") return <Navigate to="/faculty" replace />;
  if (role === "coordinator") return <Navigate to="/coordinator" replace />;
  return <Navigate to="/student" replace />;
}

/* ---------- PRIVATE ROUTE ---------- */

function PrivateRoute({ children }) {

return hasValidToken() ? children : <Navigate to="/login" />

}


/* ---------- ROLE ROUTE ---------- */

function RoleRoute({ role, children }) {

const userRole = getNormalizedRole();

return userRole === role ? children : <Navigate to="/dashboard" />

}


/* ---------- APP ---------- */

function App() {

return (

<Router>

<Routes>

{/* LOGIN + REGISTER */}

<Route path="/" element={<Login />} />
<Route path="/login" element={<Login />} />

<Route path="/register" element={<Register />} />

{/* ROLE DASHBOARD REDIRECT */}
<Route
path="/dashboard"
element={
<PrivateRoute>
<DashboardRedirect />
</PrivateRoute>
}
/>

{/* STUDENT */}

<Route
path="/student"
element={
<PrivateRoute>
<RoleRoute role="student">
<StudentDashboard/>
</RoleRoute>
</PrivateRoute>
}
/>

<Route
path="/browse"
element={
<PrivateRoute>
<RoleRoute role="student">
<BrowseNotice/>
</RoleRoute>
</PrivateRoute>
}
/>


{/* FACULTY */}

<Route
path="/faculty"
element={
<PrivateRoute>
<RoleRoute role="faculty">
<FacultyDashboard/>
</RoleRoute>
</PrivateRoute>
}
/>

<Route
path="/post-notice"
element={
<PrivateRoute>
<RoleRoute role="faculty">
<PostNotice/>
</RoleRoute>
</PrivateRoute>
}
/>


{/* ADMIN */}

<Route
path="/admin"
element={
<PrivateRoute>
<RoleRoute role="admin">
<AdminDashboard/>
</RoleRoute>
</PrivateRoute>
}
/>

<Route
path="/admin/post-notice"
element={
<PrivateRoute>
<RoleRoute role="admin">
<AdminPostNotice/>
</RoleRoute>
</PrivateRoute>
}
/>

<Route
path="/admin/manage-notices"
element={
<PrivateRoute>
<RoleRoute role="admin">
<ManageNotices/>
</RoleRoute>
</PrivateRoute>
}
/>

<Route
path="/manage-users"
element={
<PrivateRoute>
<RoleRoute role="admin">
<ManageUsers/>
</RoleRoute>
</PrivateRoute>
}
/>


{/* COORDINATOR */}

<Route
path="/coordinator"
element={
<PrivateRoute>
<RoleRoute role="coordinator">
<CoordinatorDashboard/>
</RoleRoute>
</PrivateRoute>
}
/>


{/* PROFILE */}

<Route
path="/profile"
element={
<PrivateRoute>
<Profile/>
</PrivateRoute>
}
/>

<Route
path="/edit-profile"
element={
<PrivateRoute>
<EditProfile/>
</PrivateRoute>
}
/>


{/* UNKNOWN ROUTE */}

<Route path="*" element={<Navigate to="/" />} />

</Routes>

</Router>

)

}

export default App
