// import React from "react";
// import { useNavigate } from "react-router-dom";

// function Navbar() {
//   const navigate = useNavigate();
//   const name = localStorage.getItem("name") || "User";
//   const role = (localStorage.getItem("role") || "student").replace("teacher", "faculty");

//   const logout = () => {
//     localStorage.removeItem("token");
//     localStorage.removeItem("role");
//     localStorage.removeItem("name");
//     localStorage.removeItem("canPostNotices");
//     navigate("/login", { replace: true });
//     window.location.reload();
//   };

//   return (
//     <header className="topbar">
//       <div>
//         <h3>Digital Notice Board</h3>
//         <p>{name} ({role})</p>
//       </div>
//       <button className="secondary-btn" onClick={logout}>Logout</button>
//     </header>
//   );
// }

// export default Navbar;
// import { useNavigate } from "react-router-dom";

// function Navbar(){

// const navigate = useNavigate();
// const role = localStorage.getItem("role");

// const logout = () => {

// localStorage.clear();
// navigate("/login");

// };

// return(

// <div style={styles.navbar}>

// <h2 style={styles.logo}>Digital Notice Board</h2>

// <div>

// <span style={styles.role}>
// {role?.toUpperCase()}
// </span>
// <a href="/profile">My Profile</a>
// <button style={styles.logout} onClick={logout}>
// Logout
// </button>

// </div>

// </div>

// );

// }

// const styles = {

// navbar:{
// display:"flex",
// justifyContent:"space-between",
// alignItems:"center",
// padding:"15px 40px",
// background:"#1d2671",
// color:"white"
// },

// logo:{
// margin:0
// },

// role:{
// marginRight:"20px"
// },

// logout:{
// padding:"8px 14px",
// border:"none",
// borderRadius:"5px",
// background:"#ff4d4d",
// color:"white",
// cursor:"pointer"
// }

// };

// export default Navbar;
// import { useNavigate } from "react-router-dom";
// import "../Navbar.css";

// function Navbar(){

// const navigate = useNavigate();

// const logout = () => {

// localStorage.clear();
// navigate("/login");

// };

// return(

// <div className="navbar">

// <div className="logo">
// Campus Notice Board
// </div>

// <div className="nav-right">

// <button onClick={()=>navigate("/profile")}>
// My Profile
// </button>

// <button onClick={logout}>
// Logout
// </button>

// </div>

// </div>

// )

// }

// export default Navbar
import { useNavigate } from "react-router-dom"
import "./Navbar.css"

function Navbar(){

const navigate = useNavigate()

const name = localStorage.getItem("name") || "User"
const role = (localStorage.getItem("role") || "student").toLowerCase().trim().replace("teacher", "faculty")

const logout = () => {

localStorage.clear()
navigate("/login")

}

return(

<div className="navbar">

<div className="logo" onClick={()=>navigate("/dashboard")}>
Campus Notice Board
</div>

<div className="nav-center">

<button onClick={()=>navigate("/dashboard")}>
Dashboard
</button>

<button onClick={()=>navigate("/profile")}>
Profile
</button>

</div>

<div className="nav-right">

<span className="user-info">
{name} ({role})
</span>

<button className="logout-btn" onClick={logout}>
Logout
</button>

</div>

</div>

)

}

export default Navbar
