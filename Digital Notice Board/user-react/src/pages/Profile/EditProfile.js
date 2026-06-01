// import {useEffect,useState} from "react"
// import axios from "axios"
// import Navbar from "../../components/Navbar/Navbar"

// function EditProfile(){

// const [user,setUser] = useState({})

// const userId = localStorage.getItem("userId")

// useEffect(()=>{

// axios.get(`http://localhost:5000/api/users/profile/${userId}`)
// .then(res=>setUser(res.data))

// },[])


// const updateProfile = async()=>{

// await axios.put(

// `http://localhost:5000/api/users/update/${userId}`,
// user

// )

// alert("Profile Updated")

// }


// return(

// <div>

// <Navbar/>

// <h2>Edit Profile</h2>

// <input
// value={user.name || ""}
// onChange={e=>setUser({...user,name:e.target.value})}
// />

// <br/><br/>

// <input
// value={user.username || ""}
// onChange={e=>setUser({...user,username:e.target.value})}
// />

// <br/><br/>

// <input
// value={user.email || ""}
// onChange={e=>setUser({...user,email:e.target.value})}
// />

// <br/><br/>

// <input
// value={user.phoneNumber || ""}
// onChange={e=>setUser({...user,phoneNumber:e.target.value})}
// />

// <br/><br/>

// <button onClick={updateProfile}>
// Save Changes
// </button>

// </div>

// )

// }

// export default EditProfile
import {useEffect,useState} from "react"
import {getProfile,updateProfile} from "../../services/api"
import Navbar from "../../components/Navbar/Navbar"
import {useNavigate} from "react-router-dom"

function EditProfile(){

const [user,setUser] = useState({})
const [loading,setLoading] = useState(false)

const navigate = useNavigate()
const userId = localStorage.getItem("userId")

useEffect(()=>{

fetchProfile()

},[])

const fetchProfile = async()=>{

try{

const res = await getProfile(userId)
setUser(res.data)

}catch(err){

console.log("Error loading profile")

}

}

const save = async()=>{

try{

setLoading(true)

await updateProfile(userId,user)

alert("Profile Updated Successfully")

navigate("/profile")

}catch(err){

alert("Failed to update profile")

}

setLoading(false)

}

return(

<div>

<Navbar/>

<div style={styles.card}>

<h2>Edit Profile</h2>

<input
style={styles.input}
placeholder="Name"
value={user.name || ""}
onChange={e=>setUser({...user,name:e.target.value})}
/>

<input
style={styles.input}
placeholder="Username"
value={user.username || ""}
onChange={e=>setUser({...user,username:e.target.value})}
/>

<input
style={styles.input}
placeholder="Email"
value={user.email || ""}
onChange={e=>setUser({...user,email:e.target.value})}
/>

<input
style={styles.input}
placeholder="Phone Number"
value={user.phoneNumber || ""}
onChange={e=>setUser({...user,phoneNumber:e.target.value})}
/>

<button
style={styles.button}
onClick={save}
disabled={loading}
>

{loading ? "Saving..." : "Save Changes"}

</button>

</div>

</div>

)

}

const styles={

card:{
width:"420px",
margin:"60px auto",
padding:"30px",
background:"white",
borderRadius:"8px",
boxShadow:"0px 8px 20px rgba(0,0,0,0.1)"
},

input:{
width:"100%",
padding:"10px",
marginBottom:"15px",
borderRadius:"6px",
border:"1px solid #ccc"
},

button:{
width:"100%",
padding:"12px",
background:"#2f80ed",
color:"white",
border:"none",
borderRadius:"6px",
cursor:"pointer",
fontSize:"16px"
}

}

export default EditProfile