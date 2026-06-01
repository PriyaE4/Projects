// import { useState } from "react";
// import axios from "axios";

// function PostNotice(){

// const [title,setTitle] = useState("");
// const [description,setDescription] = useState("");
// const [category,setCategory] = useState("General");
// const [expiryDate,setExpiryDate] = useState("");
// const [image,setImage] = useState(null);

// const submitNotice = async () => {

// try{

// const formData = new FormData();

// formData.append("title",title);
// formData.append("description",description);
// formData.append("category",category);
// formData.append("expiryDate",expiryDate);
// formData.append("image",image);

// await axios.post(
// "http://localhost:5000/api/notices/create",
// formData,
// {
// headers:{
// "Content-Type":"multipart/form-data"
// }
// }
// );

// alert("Notice Posted Successfully ✅");

// setTitle("");
// setDescription("");
// setCategory("General");
// setExpiryDate("");
// setImage(null);

// }
// catch(err){

// alert("Failed to post notice");

// }

// };

// return(

// <div style={styles.page}>

// <div style={styles.card}>

// <h2 style={styles.title}>Post New Notice</h2>

// <input
// style={styles.input}
// placeholder="Notice Title"
// value={title}
// onChange={(e)=>setTitle(e.target.value)}
// />

// <textarea
// style={styles.textarea}
// placeholder="Notice Description"
// value={description}
// onChange={(e)=>setDescription(e.target.value)}
// />

// <select
// style={styles.input}
// value={category}
// onChange={(e)=>setCategory(e.target.value)}
// >

// <option value="General">General</option>
// <option value="Events">Events</option>
// <option value="Hackathons">Hackathons</option>
// <option value="Holidays">Holidays</option>

// </select>

// <label style={styles.label}>
// Expiry Date
// </label>

// <input
// type="date"
// style={styles.input}
// value={expiryDate}
// onChange={(e)=>setExpiryDate(e.target.value)}
// />

// <label style={styles.label}>
// Upload Poster Image
// </label>

// <input
// type="file"
// style={styles.file}
// onChange={(e)=>setImage(e.target.files[0])}
// />

// <button
// style={styles.button}
// onClick={submitNotice}
// >

// Post Notice

// </button>

// </div>

// </div>

// );

// }


// const styles = {

// page:{
// display:"flex",
// justifyContent:"center",
// alignItems:"center",
// padding:"40px",
// background:"#f5f7fb",
// minHeight:"100vh"
// },

// card:{
// background:"white",
// padding:"30px",
// borderRadius:"10px",
// width:"400px",
// boxShadow:"0 8px 20px rgba(0,0,0,0.1)"
// },

// title:{
// textAlign:"center",
// marginBottom:"20px"
// },

// input:{
// width:"100%",
// padding:"10px",
// marginBottom:"15px",
// borderRadius:"6px",
// border:"1px solid #ccc"
// },

// textarea:{
// width:"100%",
// padding:"10px",
// height:"100px",
// marginBottom:"15px",
// borderRadius:"6px",
// border:"1px solid #ccc"
// },

// file:{
// marginBottom:"20px"
// },

// label:{
// fontSize:"14px",
// color:"#555"
// },

// button:{
// width:"100%",
// padding:"12px",
// background:"#2f80ed",
// border:"none",
// color:"white",
// fontSize:"16px",
// borderRadius:"6px",
// cursor:"pointer"
// }

// };

// export default PostNotice;
import {useState} from "react"
import {createNotice} from "../../services/api"

function PostNotice({refreshNotices}){

const [title,setTitle] = useState("")
const [description,setDescription] = useState("")
const [category,setCategory] = useState("General")
const [expiryDate,setExpiryDate] = useState("")
const [image,setImage] = useState(null)

const submitNotice = async()=>{

try{

if(image){
const formData = new FormData()
formData.append("title",title)
formData.append("description",description)
formData.append("category",category)
formData.append("expiryDate",expiryDate || "")
formData.append("image",image)
await createNotice(formData)
}else{
await createNotice({
title,
content: description,
category,
expiryDate: expiryDate || null
})
}

alert("Notice Posted Successfully")

setTitle("")
setDescription("")
setCategory("General")
setExpiryDate("")
setImage(null)

if(refreshNotices) refreshNotices()

}
catch(err){

alert("Failed to post notice")

}

}

return(

<div style={styles.card}>

<h2>Post Notice</h2>

<input
style={styles.input}
placeholder="Title"
value={title}
onChange={e=>setTitle(e.target.value)}
/>

<textarea
style={styles.textarea}
placeholder="Description"
value={description}
onChange={e=>setDescription(e.target.value)}
/>

<select
style={styles.input}
value={category}
onChange={e=>setCategory(e.target.value)}
>

<option value="General">General</option>
<option value="Events">Events</option>
<option value="Hackathons">Hackathons</option>
<option value="Holidays">Holidays</option>

</select>

<input
type="date"
style={styles.input}
value={expiryDate}
onChange={e=>setExpiryDate(e.target.value)}
/>

<input
type="file"
style={styles.input}
onChange={e=>setImage(e.target.files[0])}
/>

<button
style={styles.button}
onClick={submitNotice}
>

Post Notice

</button>

</div>

)

}

const styles={

card:{
padding:"20px",
background:"white",
margin:"20px",
borderRadius:"8px",
boxShadow:"0 4px 10px rgba(0,0,0,0.1)"
},

input:{
width:"100%",
padding:"10px",
marginBottom:"10px"
},

textarea:{
width:"100%",
height:"100px",
padding:"10px",
marginBottom:"10px"
},

button:{
padding:"10px 20px",
background:"#2f80ed",
border:"none",
color:"white",
cursor:"pointer"
}

}

export default PostNotice
