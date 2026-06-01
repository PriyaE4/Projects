import {useEffect,useMemo,useState} from "react"
import {getCoordinators,getStudents,makeCoordinator,removeCoordinator} from "../../services/api"

function ManageCoordinators(){

const [students,setStudents] = useState([])
const [coordinators,setCoordinators] = useState([])
const [error,setError] = useState("")
const [studentsError,setStudentsError] = useState("")
const [coordinatorsError,setCoordinatorsError] = useState("")
const [loading,setLoading] = useState(false)
const [studentsQuery,setStudentsQuery] = useState("")
const [coordinatorsQuery,setCoordinatorsQuery] = useState("")

useEffect(()=>{

fetchAll()

},[])

const fetchAll = async()=>{

setLoading(true)
setError("")
setStudentsError("")
setCoordinatorsError("")

const [studentsRes,coordinatorsRes] = await Promise.allSettled([
  getStudents(),
  getCoordinators()
])

let hadAnySuccess = false

if(studentsRes.status === "fulfilled"){
  setStudents(studentsRes.value?.data || [])
  hadAnySuccess = true
}else{
  setStudents([])
  setStudentsError(String(studentsRes.reason?.response?.data || studentsRes.reason?.message || "Failed to load students"))
}

if(coordinatorsRes.status === "fulfilled"){
  setCoordinators(coordinatorsRes.value?.data || [])
  hadAnySuccess = true
}else{
  setCoordinators([])
  setCoordinatorsError(String(coordinatorsRes.reason?.response?.data || coordinatorsRes.reason?.message || "Failed to load coordinators"))
}

// Only show an error if everything failed.
if(!hadAnySuccess){
  const err = studentsRes.status === "rejected" ? studentsRes.reason : coordinatorsRes.reason
  if(!err?.response && err?.message === "Network Error"){
    setError("Network Error: backend not reachable. Start backend on port 5000 (or set REACT_APP_API_BASE_URL).")
  }else{
    setError(err?.response?.data || err.message || "Failed to load permissions data")
  }
}

setLoading(false)

}

const grant = async(id)=>{

try{
await makeCoordinator(id)
await fetchAll()
}catch(err){
alert(String(err?.response?.data || err.message || "Failed to grant access"))
return
}

alert("Coordinator granted")

}

const remove = async(id)=>{

try{
await removeCoordinator(id)
await fetchAll()
}catch(err){
alert(String(err?.response?.data || err.message || "Failed to remove access"))
return
}

alert("Coordinator removed")

}

const coordinatorIds = useMemo(()=> new Set((coordinators || []).map(c=>String(c?._id))),[coordinators])

const filteredStudents = useMemo(()=>{
const q = studentsQuery.trim().toLowerCase()
let list = (students || []).filter(s=>!coordinatorIds.has(String(s?._id)))
if(!q) return list
return list.filter(s=>{
const hay = [
s?.name,
s?.email,
s?.username,
s?.rollNumber,
s?.branch,
s?.phoneNumber
].filter(Boolean).join(" ").toLowerCase()
return hay.includes(q)
})
},[students,studentsQuery,coordinatorIds])

const filteredCoordinators = useMemo(()=>{
const q = coordinatorsQuery.trim().toLowerCase()
const list = coordinators || []
if(!q) return list
return list.filter(c=>{
const hay = [
c?.name,
c?.email,
c?.username,
c?.rollNumber,
c?.branch,
c?.phoneNumber
].filter(Boolean).join(" ").toLowerCase()
return hay.includes(q)
})
},[coordinators,coordinatorsQuery])

return(

<div className="page-shell">

<div className="card">
<div className="dashboard-top">
<div>
<h3 style={{margin:"0"}}>Coordinator Permissions</h3>
<p className="subtitle">Grant selected students the right to post notices. Revoke anytime.</p>
</div>
</div>

{error ? <p style={{color:"red"}}>{String(error)}</p> : null}

<div style={{marginTop:"12px"}}>
<label style={{marginTop:"0"}}>Search (Students Without Permission)</label>
<input
value={studentsQuery}
onChange={(e)=>setStudentsQuery(e.target.value)}
placeholder="Search by name/email/roll/branch/phone"
/>
</div>

{loading ? <p className="muted-text" style={{marginTop:"10px"}}>Loading...</p> : null}

<div style={{marginTop:"14px"}}>
<h4 style={{margin:"0 0 10px"}}>Students Without Permission</h4>
{studentsError ? <p className="error-text" style={{margin:"0 0 10px"}}>{studentsError}</p> : null}
<div style={{overflowX:"auto"}}>
  <table border="1" cellPadding="10" style={{width:"100%",borderCollapse:"collapse"}}>
    <thead>
      <tr style={{background:"#f2f6ff"}}>
        <th align="left">Name</th>
        <th align="left">Email</th>
        <th align="left">Branch</th>
        <th align="left">Roll No</th>
        <th align="left">Phone</th>
        <th align="left">Action</th>
      </tr>
    </thead>
    <tbody>
      {filteredStudents.length===0 ? (
        <tr>
          <td colSpan={6} className="muted-text">No students without permission.</td>
        </tr>
      ) : (
        filteredStudents.map((s)=>(
          <tr key={s._id}>
            <td>{s.name}</td>
            <td>{s.email}</td>
            <td>{s.branch || "-"}</td>
            <td>{s.rollNumber || "-"}</td>
            <td>{s.phoneNumber || "-"}</td>
            <td>
              <button className="secondary-btn inline-btn" onClick={()=>grant(s._id)}>
                Grant
              </button>
            </td>
          </tr>
        ))
      )}
    </tbody>
  </table>
</div>
</div>

<div style={{marginTop:"18px"}}>
<h4 style={{margin:"0 0 10px"}}>Students With Permission (Coordinators)</h4>
<div style={{margin:"0 0 10px"}}>
  <label style={{margin:"0 0 6px"}}>Search (Coordinators)</label>
  <input
    value={coordinatorsQuery}
    onChange={(e)=>setCoordinatorsQuery(e.target.value)}
    placeholder="Search coordinators by name/email/roll/branch/phone"
  />
</div>
{coordinatorsError ? <p className="error-text" style={{margin:"0 0 10px"}}>{coordinatorsError}</p> : null}
<div style={{overflowX:"auto"}}>
  <table border="1" cellPadding="10" style={{width:"100%",borderCollapse:"collapse"}}>
    <thead>
      <tr style={{background:"#fff0f0"}}>
        <th align="left">Name</th>
        <th align="left">Email</th>
        <th align="left">Branch</th>
        <th align="left">Roll No</th>
        <th align="left">Phone</th>
        <th align="left">Action</th>
      </tr>
    </thead>
    <tbody>
      {filteredCoordinators.length===0 ? (
        <tr>
          <td colSpan={6} className="muted-text">No coordinators with permission.</td>
        </tr>
      ) : (
        filteredCoordinators.map((c)=>(
          <tr key={c._id}>
            <td>{c.name}</td>
            <td>{c.email}</td>
            <td>{c.branch || "-"}</td>
            <td>{c.rollNumber || "-"}</td>
            <td>{c.phoneNumber || "-"}</td>
            <td>
              <button className="danger-btn inline-btn" onClick={()=>remove(c._id)}>
                Remove
              </button>
            </td>
          </tr>
        ))
      )}
    </tbody>
  </table>
</div>
</div>

</div>
</div>

)

}

export default ManageCoordinators
