// import React, { useEffect, useState } from "react";
// import { Link, useNavigate } from "react-router-dom";
// import api from "../utils/api";

// function Login() {
//   const [loginData, setLoginData] = useState({
//     identifier: "",
//     password: ""
//   });
//   const [isLoading, setIsLoading] = useState(false);
//   const [error, setError] = useState("");

//   const navigate = useNavigate();

//   useEffect(() => {
//     if (localStorage.getItem("token")) {
//       navigate("/dashboard", { replace: true });
//     }
//   }, [navigate]);

//   const handleChange = (e) => {
//     setError("");
//     setLoginData({
//       ...loginData,
//       [e.target.name]: e.target.value
//     });
//   };

//   const login = async (e) => {
//     e.preventDefault();

//     if (!loginData.identifier || !loginData.password) {
//       setError("Please enter username/email and password.");
//       return;
//     }

//     try {
//       setIsLoading(true);
//       const normalizedIdentifier = loginData.identifier.trim();
//       const res = await api.post("/auth/login", {
//         identifier: normalizedIdentifier,
//         email: normalizedIdentifier,
//         username: normalizedIdentifier,
//         password: loginData.password
//       });

//       localStorage.setItem("token", res.data.token);
//       localStorage.setItem("role", (res.data.user.role || "").replace("teacher", "faculty"));
//       localStorage.setItem("name", res.data.user.name);
//       localStorage.setItem("canPostNotices", String(res.data.user.canPostNotices));

//       navigate("/dashboard", { replace: true });
//     } catch (error) {
//       setError(error.response?.data?.message || "Invalid credentials");
//     } finally {
//       setIsLoading(false);
//     }
//   };

//   return (
//     <div className="page-shell">
//       <section className="card login-card">
//         <h1>Campus Digital Notice Board</h1>
//         <p className="subtitle">Sign in to view official college notices</p>

//         <form onSubmit={login}>
//           <label htmlFor="identifier">Username or Email</label>
//           <input
//             id="identifier"
//             type="text"
//             name="identifier"
//             placeholder="admin or user@college.edu"
//             value={loginData.identifier}
//             onChange={handleChange}
//           />

//           <label htmlFor="password">Password</label>
//           <input
//             id="password"
//             type="password"
//             name="password"
//             placeholder="Enter password"
//             value={loginData.password}
//             onChange={handleChange}
//           />

//           {error ? <p className="error-text">{error}</p> : null}

//           <button className="primary-btn" type="submit" disabled={isLoading}>
//             {isLoading ? "Signing in..." : "Login"}
//           </button>
//         </form>

//         <p className="auth-link">
//           Student/Faculty new here? <Link to="/register">Create account</Link>
//         </p>
//       </section>
//     </div>
//   );
// }

// import { useState } from "react";
// import axios from "axios";
// import {loginUser} from "../../services/api"
// import { useNavigate } from "react-router-dom";

// function Login(){

// const [role,setRole] = useState("student");
// const [email,setEmail] = useState("");
// const [password,setPassword] = useState("");

// const navigate = useNavigate();

// const login = async () => {

// try{

// const res = await axios.post(
// "http://localhost:5000/api/auth/login",
// {
// email,
// password,
// role
// }
// );

// localStorage.setItem("token",res.data.token);
// localStorage.setItem("userId", res.data._id);
// localStorage.setItem("role",role);

// if(role === "admin"){
// navigate("/admin")
// }
// else if(role === "faculty"){
// navigate("/faculty")
// }
// else if(role === "coordinator"){
// navigate("/coordinator")
// }
// else{
// navigate("/student")
// }

// }

// catch(err){
// alert("Invalid Login Credentials")
// }

// };

// return(

// <div style={styles.page}>

// <div style={styles.card}>

// <h1 style={styles.title}>Digital Notice Board</h1>

// <p style={styles.subtitle}>Campus announcements in one place</p>

// <h3>Login</h3>

// {/* ROLE SELECTOR */}

// <div style={styles.roleBox}>

// <button
// style={role==="admin"?styles.activeRole:styles.roleBtn}
// onClick={()=>setRole("admin")}
// >
// Admin
// </button>

// <button
// style={role==="faculty"?styles.activeRole:styles.roleBtn}
// onClick={()=>setRole("faculty")}
// >
// Faculty
// </button>

// <button
// style={role==="student"?styles.activeRole:styles.roleBtn}
// onClick={()=>setRole("student")}
// >
// Student
// </button>

// </div>

// <input
// style={styles.input}
// placeholder="Email"
// onChange={(e)=>setEmail(e.target.value)}
// />

// <input
// style={styles.input}
// type="password"
// placeholder="Password"
// onChange={(e)=>setPassword(e.target.value)}
// />

// <button style={styles.loginBtn} onClick={login}>
// Login
// </button>

// <p style={{marginTop:"15px"}}>

// Don't have an account?

// <a href="/register" style={styles.link}>
//  Register
// </a>

// </p>

// </div>

// </div>

// );

// }

// const styles = {

// page:{
// height:"100vh",
// display:"flex",
// justifyContent:"center",
// alignItems:"center",
// background:"linear-gradient(135deg,#1d2671,#c33764)"
// },

// card:{
// background:"white",
// padding:"40px",
// borderRadius:"12px",
// width:"350px",
// textAlign:"center",
// boxShadow:"0px 8px 25px rgba(0,0,0,0.2)"
// },

// title:{
// marginBottom:"5px",
// color:"#333"
// },

// subtitle:{
// fontSize:"14px",
// color:"#666",
// marginBottom:"20px"
// },

// roleBox:{
// display:"flex",
// justifyContent:"center",
// gap:"10px",
// marginBottom:"20px"
// },

// roleBtn:{
// padding:"8px 14px",
// border:"1px solid #ccc",
// background:"white",
// cursor:"pointer",
// borderRadius:"6px"
// },

// activeRole:{
// padding:"8px 14px",
// border:"none",
// background:"#2f80ed",
// color:"white",
// cursor:"pointer",
// borderRadius:"6px"
// },

// input:{
// width:"100%",
// padding:"10px",
// marginBottom:"15px",
// borderRadius:"6px",
// border:"1px solid #ccc"
// },

// loginBtn:{
// width:"100%",
// padding:"12px",
// border:"none",
// background:"#2f80ed",
// color:"white",
// borderRadius:"6px",
// cursor:"pointer",
// fontSize:"16px"
// },

// link:{
// color:"#2f80ed",
// marginLeft:"5px",
// textDecoration:"none"
// }

// }

// export default Login;

import {useState} from "react"
import {loginUser} from "../../services/api"
import {useNavigate} from "react-router-dom"
import "./Login.css"

function Login(){

const [data,setData]=useState({
identifier:"",
password:""
})

const [error,setError]=useState("")

const navigate=useNavigate()

const login=async()=>{

try{

setError("")
const res=await loginUser({
...data,
identifier: data.identifier.trim()
})

localStorage.setItem("token",res.data.token)
localStorage.setItem("userId",res.data.user?.id)
localStorage.setItem("role",res.data.user?.role)
localStorage.setItem("name",res.data.user?.name)
localStorage.setItem("canPostNotices", String(res.data.user?.canPostNotices))

if(res.data.user?.role==="student") navigate("/student")
else if(res.data.user?.role==="faculty") navigate("/faculty")
else if(res.data.user?.role==="admin") navigate("/admin")
else if(res.data.user?.role==="coordinator") navigate("/coordinator")

}catch(err){

setError(err.response?.data || err.message || "Login failed")

}

}

return(

<div className="login-page">

<div className="login-card">

<h1>BVRITH Notice Board</h1>

<p className="subtitle">
Login to view notices and announcements
</p>

<input
type="text"
placeholder="Email or Username"
onChange={e=>setData({...data,identifier:e.target.value})}
/>

<input
type="password"
placeholder="Password"
onChange={e=>setData({...data,password:e.target.value})}
/>

{error && <p className="error">{error}</p>}

<button onClick={login}>
Login
</button>

<p className="register-link">

Don't have an account?

<a href="/register">
Register
</a>

</p>

</div>

</div>

)

}

export default Login
