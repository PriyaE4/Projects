// import React, { useEffect, useState } from "react";
// import { Link, useNavigate } from "react-router-dom";
// import api from "../utils/api";

// function Register() {
//   const navigate = useNavigate();
//   const [formData, setFormData] = useState({
//     name: "",
//     username: "",
//     email: "",
//     phoneNumber: "",
//     branch: "",
//     rollNumber: "",
//     password: "",
//     confirmPassword: "",
//     role: "student"
//   });
//   const [error, setError] = useState("");
//   const [success, setSuccess] = useState("");
//   const [isLoading, setIsLoading] = useState(false);

//   useEffect(() => {
//     if (localStorage.getItem("token")) {
//       navigate("/dashboard", { replace: true });
//     }
//   }, [navigate]);

//   const handleChange = (e) => {
//     setError("");
//     setSuccess("");
//     setFormData((prev) => ({
//       ...prev,
//       [e.target.name]: e.target.value
//     }));
//   };

//   const handleSubmit = async (e) => {
//     e.preventDefault();

//     if (!formData.name || !formData.email || !formData.password) {
//       setError("Name, email, and password are required.");
//       return;
//     }

//     if (!formData.phoneNumber) {
//       setError("Phone number is required.");
//       return;
//     }

//     if (formData.role === "student" && (!formData.branch || !formData.rollNumber)) {
//       setError("Branch and roll number are required for students.");
//       return;
//     }

//     if (formData.password !== formData.confirmPassword) {
//       setError("Password and confirm password must match.");
//       return;
//     }

//     try {
//       setIsLoading(true);
//       await api.post("/auth/register", {
//         name: formData.name,
//         username: formData.username,
//         email: formData.email,
//         phoneNumber: formData.phoneNumber,
//         branch: formData.role === "student" ? formData.branch : "",
//         rollNumber: formData.role === "student" ? formData.rollNumber : "",
//         password: formData.password,
//         role: formData.role
//       });

//       setSuccess("Registration successful. Please login.");
//       setTimeout(() => {
//         navigate("/login", { replace: true });
//       }, 700);
//     } catch (err) {
//       setError(err.response?.data?.message || "Unable to register");
//     } finally {
//       setIsLoading(false);
//     }
//   };

//   return (
//     <div className="page-shell">
//       <section className="card login-card">
//         <h1>Create Account</h1>
//         <p className="subtitle">Register as student or faculty (admin registration disabled)</p>

//         <form onSubmit={handleSubmit}>
//           <label htmlFor="name">Full Name</label>
//           <input
//             id="name"
//             name="name"
//             type="text"
//             value={formData.name}
//             onChange={handleChange}
//             placeholder="Your full name"
//           />

//           <label htmlFor="username">Username (optional)</label>
//           <input
//             id="username"
//             name="username"
//             type="text"
//             value={formData.username}
//             onChange={handleChange}
//             placeholder="e.g. anita.mech"
//           />

//           <label htmlFor="email">Email</label>
//           <input
//             id="email"
//             name="email"
//             type="email"
//             value={formData.email}
//             onChange={handleChange}
//             placeholder="you@college.edu"
//           />

//           <label htmlFor="phoneNumber">Phone Number</label>
//           <input
//             id="phoneNumber"
//             name="phoneNumber"
//             type="tel"
//             value={formData.phoneNumber}
//             onChange={handleChange}
//             placeholder="10-digit number"
//           />

//           {formData.role === "student" ? (
//             <>
//               <label htmlFor="branch">Branch</label>
//               <input
//                 id="branch"
//                 name="branch"
//                 type="text"
//                 value={formData.branch}
//                 onChange={handleChange}
//                 placeholder="CSE / ECE / MECH..."
//               />

//               <label htmlFor="rollNumber">Roll Number</label>
//               <input
//                 id="rollNumber"
//                 name="rollNumber"
//                 type="text"
//                 value={formData.rollNumber}
//                 onChange={handleChange}
//                 placeholder="College roll number"
//               />
//             </>
//           ) : null}

//           <label htmlFor="role">Role</label>
//           <select id="role" name="role" value={formData.role} onChange={handleChange}>
//             <option value="student">Student</option>
//             <option value="faculty">Faculty</option>
//           </select>

//           <label htmlFor="password">Password</label>
//           <input
//             id="password"
//             name="password"
//             type="password"
//             value={formData.password}
//             onChange={handleChange}
//             placeholder="Create password"
//           />

//           <label htmlFor="confirmPassword">Confirm Password</label>
//           <input
//             id="confirmPassword"
//             name="confirmPassword"
//             type="password"
//             value={formData.confirmPassword}
//             onChange={handleChange}
//             placeholder="Re-enter password"
//           />

//           {error ? <p className="error-text">{error}</p> : null}
//           {success ? <p className="success-text">{success}</p> : null}

//           <button className="primary-btn" type="submit" disabled={isLoading}>
//             {isLoading ? "Registering..." : "Register"}
//           </button>
//         </form>

//         <p className="auth-link">
//           Already have an account? <Link to="/login">Login</Link>
//         </p>
//       </section>
//     </div>
//   );
// }

// export default Register;
// import { useState } from "react";
// import axios from "axios";
// import { useNavigate } from "react-router-dom";

// function Register(){

// const navigate = useNavigate();

// const [form,setForm] = useState({

// name:"",
// username:"",
// email:"",
// phoneNumber:"",
// branch:"",
// rollNumber:"",
// password:"",
// confirmPassword:"",
// role:"student"

// });


// const handleChange = (e)=>{

// setForm({...form,[e.target.name]:e.target.value})

// }


// const register = async ()=>{

// if(form.password !== form.confirmPassword){

// alert("Passwords do not match");
// return;

// }

// try{

// await axios.post(
// "http://localhost:5000/api/auth/register",
// form
// );

// alert("Registration Successful")

// navigate("/login")

// }

// catch(err){

// alert("Registration Failed")

// }

// }



// return(

// <div style={styles.page}>

// <div style={styles.card}>

// <h1 style={styles.title}>Digital Notice Board</h1>

// <p style={styles.subtitle}>
// Create your account
// </p>


// {/* ROLE SELECTOR */}

// <div style={styles.roleBox}>

// <button
// style={form.role==="admin"?styles.activeRole:styles.roleBtn}
// onClick={()=>setForm({...form,role:"admin"})}
// >
// Admin
// </button>

// <button
// style={form.role==="faculty"?styles.activeRole:styles.roleBtn}
// onClick={()=>setForm({...form,role:"faculty"})}
// >
// Faculty
// </button>

// <button
// style={form.role==="student"?styles.activeRole:styles.roleBtn}
// onClick={()=>setForm({...form,role:"student"})}
// >
// Student
// </button>

// </div>


// {/* BASIC FIELDS */}

// <input
// style={styles.input}
// placeholder="Full Name"
// name="name"
// onChange={handleChange}
// />

// <input
// style={styles.input}
// placeholder="Username"
// name="username"
// onChange={handleChange}
// />

// <input
// style={styles.input}
// placeholder="Email"
// name="email"
// onChange={handleChange}
// />


// {/* STUDENT ONLY FIELDS */}

// {form.role==="student" && (

// <>

// <input
// style={styles.input}
// placeholder="Phone Number"
// name="phoneNumber"
// onChange={handleChange}
// />

// <input
// style={styles.input}
// placeholder="Branch"
// name="branch"
// onChange={handleChange}
// />

// <input
// style={styles.input}
// placeholder="Roll Number"
// name="rollNumber"
// onChange={handleChange}
// />

// </>

// )}


// {/* PASSWORD */}

// <input
// style={styles.input}
// type="password"
// placeholder="Password"
// name="password"
// onChange={handleChange}
// />

// <input
// style={styles.input}
// type="password"
// placeholder="Confirm Password"
// name="confirmPassword"
// onChange={handleChange}
// />


// <button style={styles.registerBtn} onClick={register}>

// Register

// </button>


// <p style={{marginTop:"15px"}}>

// Already have account?

// <a href="/login" style={styles.link}>

//  Login

// </a>

// </p>

// </div>

// </div>

// )

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
// width:"380px",
// maxHeight:"90vh",
// overflowY:"auto",
// textAlign:"center",
// boxShadow:"0px 10px 25px rgba(0,0,0,0.25)"
// },

// title:{
// marginBottom:"5px"
// },

// subtitle:{
// color:"#777",
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
// marginBottom:"12px",
// borderRadius:"6px",
// border:"1px solid #ccc"
// },

// registerBtn:{
// width:"100%",
// padding:"12px",
// background:"#2f80ed",
// border:"none",
// color:"white",
// fontSize:"16px",
// borderRadius:"6px",
// cursor:"pointer"
// },

// link:{
// color:"#2f80ed",
// textDecoration:"none",
// marginLeft:"5px"
// }

// }

// export default Register;

import { useState } from "react"
import { registerUser } from "../../services/api"
import "./Login.css"
import "./Register.css"

function Register(){

const [data,setData] = useState({
name:"",
email:"",
username:"",
phoneNumber:"",
branch:"",
rollNumber:"",
password:"",
confirmPassword:"",
role:"student"
})

const [error,setError] = useState("")
const [success,setSuccess] = useState("")

const register = async()=>{

setError("")
setSuccess("")

if(data.password !== data.confirmPassword){
setError("Passwords do not match")
return
}

try{

const payload = {
...data,
name: data.name.trim(),
email: data.email.trim(),
username: data.username.trim(),
phoneNumber: data.phoneNumber.trim(),
branch: data.branch.trim(),
rollNumber: data.rollNumber.trim(),
};

if(payload.role !== "student"){
payload.branch = ""
payload.rollNumber = ""
}

await registerUser(payload)

setSuccess("Registered successfully. You can login now.")

}catch(err){

setError(err.response?.data || err.message || "Registration failed")

}

}

return(

<div className="login-page">

<div className="login-card register-card">

<h1>BVRITH Notice Board</h1>

<p className="subtitle">
Create your account to access notices and announcements
</p>

<input
type="text"
placeholder="Full Name"
onChange={e=>setData({...data,name:e.target.value})}
/>

<input
type="email"
placeholder="Email"
onChange={e=>setData({...data,email:e.target.value})}
/>

<input
placeholder="Username"
onChange={e=>setData({...data,username:e.target.value})}
/>

<input
placeholder="Phone Number"
onChange={e=>setData({...data,phoneNumber:e.target.value})}
/>

{/* Branch only for students */}

{data.role === "student" && (

<>
<input
placeholder="Branch"
onChange={e=>setData({...data,branch:e.target.value})}
/>
</>

)}

<input
placeholder="Roll Number / Employee ID"
onChange={e=>setData({...data,rollNumber:e.target.value})}
/>

<input
placeholder="Password"
type="password"
onChange={e=>setData({...data,password:e.target.value})}
/>

<input
placeholder="Confirm Password"
type="password"
onChange={e=>setData({...data,confirmPassword:e.target.value})}
/>

{error && <p className="error">{error}</p>}
{success && <p className="success">{success}</p>}

<select
onChange={e=>setData({...data,role:e.target.value})}
>

<option value="student">Student</option>
<option value="faculty">Faculty</option>
<option value="admin">Admin</option>

</select>

<button onClick={register}>
Register
</button>

<p className="register-link">
Already have an account?
<a href="/login">Login</a>
</p>

</div>

</div>

)

}

export default Register
