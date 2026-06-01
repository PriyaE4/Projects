import Navbar from "../../components/Navbar/Navbar"
import PostNotice from "../Faculty/PostNotice"

function AdminPostNotice(){

return(

<div>

<Navbar/>

<div className="page-shell">
<div className="card">
<h2 style={{margin:"0 0 6px"}}>Post Notice</h2>
<p className="subtitle">Create a new notice as Admin.</p>
<PostNotice/>
</div>
</div>

</div>

)

}

export default AdminPostNotice

