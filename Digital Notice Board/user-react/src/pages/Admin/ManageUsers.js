// import {useEffect,useState} from "react"
// import axios from "axios"

// function ManageUsers(){

// const [users,setUsers] = useState([])

// useEffect(()=>{

// axios.get("http://localhost:5000/api/users/all")
// .then(res=>setUsers(res.data))

// },[])

// const deleteUser = async(id)=>{

// await axios.delete(
// "http://localhost:5000/api/users/"+id
// )

// alert("User removed")

// }

// return(

// <div>

// <h3>Manage Users</h3>

// {users.map(u => (

// <div key={u._id}>

// {u.name} - {u.role}

// <button onClick={()=>deleteUser(u._id)}>
// Remove
// </button>

// </div>

// ))}

// </div>

// )

// }

// export default ManageUsers
import {useEffect,useMemo,useState} from "react"
import Navbar from "../../components/Navbar/Navbar"
import "./ManageUsers.css"
import {deleteUser as apiDeleteUser, getUsers, makeCoordinator as apiMakeCoordinator, removeCoordinator as apiRemoveCoordinator} from "../../services/api"

function ManageUsers(){

const [users,setUsers]=useState([])
const [error,setError] = useState("")
const [qAdmin,setQAdmin] = useState("")
const [qFaculty,setQFaculty] = useState("")
const [qCoordinator,setQCoordinator] = useState("")
const [qStudent,setQStudent] = useState("")
const [selectedUser,setSelectedUser] = useState(null)

useEffect(()=>{

fetchUsers()

},[])

const makeHay = (u) =>
  [
    u?.name,
    u?.email,
    u?.username,
    u?.rollNumber,
    u?.branch,
    u?.phoneNumber
  ]
    .filter(Boolean)
    .join(" ")
    .toLowerCase();

const filterByQuery = (list, query) => {
  const q = String(query || "").trim().toLowerCase();
  if (!q) return list;
  return (list || []).filter((u) => makeHay(u).includes(q));
};

const fetchUsers = async () => {

try{
setError("")
const res = await getUsers()
setUsers(res.data || [])
}catch(err){
setUsers([])
setError(String(err?.response?.data || err.message || "Failed to load users"))
}

}

const deleteUser = async(id)=>{

try{
await apiDeleteUser(id)
}catch(err){
alert(String(err?.response?.data || err.message || "Failed to delete user"))
return
}

alert("User removed")

fetchUsers()

}

const promoteToCoordinator = async(id)=>{

try{
await apiMakeCoordinator(id)
}catch(err){
alert(String(err?.response?.data || err.message || "Failed to update role"))
return
}

alert("User promoted to Coordinator")

fetchUsers()

}

const revokeCoordinator = async(id)=>{

try{
await apiRemoveCoordinator(id)
}catch(err){
alert(String(err?.response?.data || err.message || "Failed to remove coordinator"))
return
}

alert("Coordinator removed")

fetchUsers()

}

const formatDateTime = (value) => {
  if (!value) return "-";
  try {
    const d = new Date(value);
    if (Number.isNaN(d.getTime())) return String(value);
    return d.toLocaleString();
  } catch {
    return String(value);
  }
};

const admins = useMemo(()=> users.filter(u=>u.role==="admin"),[users])
const faculties = useMemo(()=> users.filter(u=>u.role==="faculty" || u.role==="teacher"),[users])
const coordinators = useMemo(()=> users.filter(u=>u.role==="coordinator"),[users])
const students = useMemo(()=> users.filter(u=>u.role==="student"),[users])

const adminsFiltered = useMemo(()=>filterByQuery(admins,qAdmin),[admins,qAdmin])
const facultiesFiltered = useMemo(()=>filterByQuery(faculties,qFaculty),[faculties,qFaculty])
const coordinatorsFiltered = useMemo(()=>filterByQuery(coordinators,qCoordinator),[coordinators,qCoordinator])
const studentsFiltered = useMemo(()=>filterByQuery(students,qStudent),[students,qStudent])

const UsersTable = ({ title, query, setQuery, rows, actionRenderer }) => (
  <div style={{marginTop:"18px"}}>
    <h3 style={{margin:"0 0 8px"}}>{title} <span style={{color:"#6b7a90",fontWeight:600}}>({rows.length})</span></h3>

    <input
      value={query}
      onChange={(e)=>setQuery(e.target.value)}
      placeholder={`Search ${title.toLowerCase()}...`}
      style={{width:"100%",maxWidth:"520px",marginBottom:"10px"}}
    />

    <div style={{overflowX:"auto"}}>
      <table className="users-table">
        <thead>
          <tr>
            <th>Name</th>
            <th>Email</th>
            <th>Role</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {rows.length===0 ? (
            <tr>
              <td colSpan={4} style={{color:"#6b7a90"}}>No users found.</td>
            </tr>
          ) : (
            rows.map((u)=>(
              <tr
              key={u._id}
              className={selectedUser?._id===u._id ? "user-row-selected" : ""}
              style={{cursor:"pointer"}}
              onClick={()=>setSelectedUser(u)}
              >
                <td>{u.name}</td>
                <td>{u.email}</td>
                <td>
                  <span className={`role-badge ${u.role}`}>
                    {u.role}
                  </span>
                </td>
                <td>
                  {actionRenderer ? actionRenderer(u) : null}
                </td>
              </tr>
            ))
          )}
        </tbody>
      </table>
    </div>
  </div>
)

return(

<div>

<Navbar/>

<div className="users-container">

<h2>Manage Users</h2>

{error ? <p className="error-text">{error}</p> : null}

{selectedUser ? (
  <div className="user-detail-card">
    <div className="user-detail-head">
      <div>
        <h3 style={{margin:"0"}}>User Details</h3>
        <p style={{margin:"4px 0 0",color:"#6b7a90"}}>Click another row to switch. This shows registration details.</p>
      </div>
      <button className="delete-btn" onClick={()=>setSelectedUser(null)}>
        Close
      </button>
    </div>

    <div className="user-detail-grid">
      <div><strong>Name:</strong> {selectedUser.name || "-"}</div>
      <div><strong>Email:</strong> {selectedUser.email || "-"}</div>
      <div><strong>Username:</strong> {selectedUser.username || "-"}</div>
      <div><strong>Role:</strong> {selectedUser.role || "-"}</div>
      <div><strong>Phone:</strong> {selectedUser.phoneNumber || "-"}</div>
      <div><strong>Branch:</strong> {selectedUser.branch || "-"}</div>
      <div><strong>Roll No:</strong> {selectedUser.rollNumber || "-"}</div>
      <div><strong>Created At:</strong> {formatDateTime(selectedUser.createdAt)}</div>
      <div><strong>Updated At:</strong> {formatDateTime(selectedUser.updatedAt)}</div>
      <div><strong>User Id:</strong> {selectedUser._id}</div>
    </div>
  </div>
) : null}


<UsersTable
title="Admins"
query={qAdmin}
setQuery={setQAdmin}
rows={adminsFiltered}
actionRenderer={() => <span style={{color:"#6b7a90"}}>No actions</span>}
/>

<UsersTable
title="Faculty"
query={qFaculty}
setQuery={setQFaculty}
rows={facultiesFiltered}
actionRenderer={(u)=>(
  <>
    {u.role !== "admin" ? (
      <button
      className="delete-btn"
      onClick={(e)=>{e.stopPropagation(); deleteUser(u._id)}}
      >
      Delete
      </button>
    ) : null}
  </>
)}
/>

<UsersTable
title="Coordinators"
query={qCoordinator}
setQuery={setQCoordinator}
rows={coordinatorsFiltered}
actionRenderer={(u)=>(
  <>
    <button
    className="coord-btn"
    onClick={(e)=>{e.stopPropagation(); revokeCoordinator(u._id)}}
    >
    Remove Coordinator
    </button>

    {u.role !== "admin" ? (
      <button
      className="delete-btn"
      onClick={(e)=>{e.stopPropagation(); deleteUser(u._id)}}
      >
      Delete
      </button>
    ) : null}
  </>
)}
/>

<UsersTable
title="Students"
query={qStudent}
setQuery={setQStudent}
rows={studentsFiltered}
actionRenderer={(u)=>(
  <>
    <button
    className="coord-btn"
    onClick={(e)=>{e.stopPropagation(); promoteToCoordinator(u._id)}}
    >
    Make Coordinator
    </button>

    {u.role !== "admin" ? (
      <button
      className="delete-btn"
      onClick={(e)=>{e.stopPropagation(); deleteUser(u._id)}}
      >
      Delete
      </button>
    ) : null}
  </>
)}
/>

</div>

</div>

)

}

export default ManageUsers
