// // import React from "react";

// // function NoticeCard({
// //   notice,
// //   canEdit,
// //   canDelete,
// //   canPin,
// //   onTogglePin,
// //   onEdit,
// //   onDelete
// // }) {

// //   const getClassName = () => {
// //     if (notice.priority === "High") return "notice-high";
// //     if (notice.priority === "Medium") return "notice-medium";
// //     return "notice-low";
// //   };

// //   const formatDate = (value) => {
// //     if (!value) return "Not specified";
// //     return new Date(value).toLocaleString();
// //   };

// //   return (
// //     <article className={`notice-card ${getClassName()}`}>
// //       <div className="notice-head">
// //         <h3>{notice.title}</h3>
// //         <div className="badge-stack">
// //           {notice.isPinned ? <span className="pinned-pill">Pinned</span> : null}
// //           <span className="priority-pill">{notice.priority || "Low"}</span>
// //         </div>
// //       </div>

// //       <p>{notice.content}</p>

// //       <div className="notice-meta">
// //         <span>Category: {notice.category || "General"}</span>
// //         <span>Posted by: {notice.createdBy?.name || "Admin"}</span>
// //         <span>Posted on: {formatDate(notice.createdAt)}</span>
// //         <span>Expires: {formatDate(notice.expiryDate)}</span>
// //       </div>

// //       {canEdit || canDelete || canPin ? (
// //         <div className="action-row">
// //           {canPin ? (
// //             <button type="button" className="secondary-btn inline-btn" onClick={onTogglePin}>
// //               {notice.isPinned ? "Unpin" : "Pin"}
// //             </button>
// //           ) : null}
// //           {canEdit ? (
// //             <button type="button" className="secondary-btn inline-btn" onClick={onEdit}>
// //               Edit
// //             </button>
// //           ) : null}
// //           {canDelete ? (
// //             <button type="button" className="danger-btn inline-btn" onClick={onDelete}>
// //               Delete
// //             </button>
// //           ) : null}
// //         </div>
// //       ) : null}
// //     </article>
// //   );
// // }

// // export default NoticeCard;
// // function NoticeCard({notice}){

// // return(

// // <div style={{
// // border:"1px solid #ddd",
// // padding:"15px",
// // borderRadius:"10px"
// // }}>

// // <h3>{notice.title}</h3>

// // <p>{notice.description}</p>

// // </div>

// // );

// // }

// // function NoticeCard({notice}){

// // return(

// // <div style={{
// // background:"white",
// // borderRadius:"10px",
// // padding:"15px",
// // boxShadow:"0 2px 10px rgba(0,0,0,0.1)"
// // }}>

// // <h3>{notice.title}</h3>

// // <p>{notice.description}</p>

// // {notice.image && (

// // <img
// // src={`http://localhost:5000/uploads/${notice.image}`}
// // alt="notice"
// // style={{
// // width:"100%",
// // marginTop:"10px",
// // borderRadius:"8px"
// // }}
// // />

// // )}

// // </div>

// // );

// // }

// // export default NoticeCard;
// function NoticeCard({notice}){

// return(

// <div style={{

// background:"white",
// padding:"20px",

// borderRadius:"10px",

// boxShadow:"0px 5px 15px rgba(0,0,0,0.1)"

// }}>

// <h3>{notice.title}</h3>

// <p>{notice.description}</p>

// <p>
// <b>Category:</b> {notice.category}
// </p>

// <p>
// <b>Priority:</b> {notice.priority}
// </p>

// {notice.image && (

// <img
// src={`http://localhost:5000/uploads/${notice.image}`}
// alt="notice"
// style={{width:"100%",marginTop:"10px"}}
// />

// )}

// </div>

// )

// }

// import "./NoticeCard.css"

// function NoticeCard({notice}){

// const getPriorityClass = () => {

// if(notice.priority === "High") return "priority-high"
// if(notice.priority === "Medium") return "priority-medium"
// return "priority-low"

// }

// return(

// <div className="notice-card">

// <div className="notice-header">

// <h3>{notice.title}</h3>

// <span className={`priority-badge ${getPriorityClass()}`}>
// {notice.priority}
// </span>

// </div>

// <p className="notice-description">
// {notice.description}
// </p>

// <div className="notice-meta">

// <span className="category-badge">
// {notice.category}
// </span>

// <span className="date">
// {new Date(notice.createdAt).toLocaleDateString()}
// </span>

// </div>

// {notice.image && (

// <img
// src={`http://localhost:5000/uploads/${notice.image}`}
// alt="notice"
// className="notice-image"
// />

// )}

// </div>

// )

// }

// export default NoticeCard





import { useEffect, useMemo, useState } from "react"
import { deleteNotice, setNoticePinned, updateNotice } from "../../services/api"
import { API_BASE_URL } from "../../services/api"

function NoticeCard({ notice, refreshNotices }) {
  const role = (localStorage.getItem("role") || "student").toLowerCase()
  const canPostNotices = (localStorage.getItem("canPostNotices") || "false") === "true"

  const canManage = useMemo(() => {
    if (["admin", "faculty", "teacher", "coordinator"].includes(role)) return true
    return role === "student" && canPostNotices
  }, [role, canPostNotices])

  const [editing, setEditing] = useState(false)
  const [title, setTitle] = useState(notice.title || "")
  const [content, setContent] = useState(notice.content || "")
  const [isSaving, setIsSaving] = useState(false)
  const [isImageOpen, setIsImageOpen] = useState(false)

  const imageSrc = notice.image ? `${API_BASE_URL}/uploads/${notice.image}` : ""

  useEffect(() => {
    if (!isImageOpen) return

    const onKeyDown = (e) => {
      if (e.key === "Escape") setIsImageOpen(false)
    }

    document.addEventListener("keydown", onKeyDown)
    const prevOverflow = document.body.style.overflow
    document.body.style.overflow = "hidden"

    return () => {
      document.removeEventListener("keydown", onKeyDown)
      document.body.style.overflow = prevOverflow
    }
  }, [isImageOpen])

  const removeNotice = async () => {
    if (!canManage) return
    await deleteNotice(notice._id)
    if (refreshNotices) refreshNotices()
  }

  const saveEdit = async () => {
    if (!canManage) return

    try {
      setIsSaving(true)
      await updateNotice(notice._id, {
        title,
        content,
        category: notice.category || "",
        priority: notice.priority || "Low",
        expiryDate: notice.expiryDate || null,
        isPinned: Boolean(notice.isPinned)
      })
      setEditing(false)
      if (refreshNotices) refreshNotices()
    } finally {
      setIsSaving(false)
    }
  }

  const togglePin = async () => {
    if (!canManage) return
    await setNoticePinned(notice._id, !notice.isPinned)
    if (refreshNotices) refreshNotices()
  }

  return (
    <>
      <div style={styles.card}>
        {editing ? (
          <>
          <input
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            placeholder="Title"
            style={styles.input}
          />

          <textarea
            value={content}
            onChange={(e) => setContent(e.target.value)}
            placeholder="Content"
            style={styles.textarea}
          />

          <div style={styles.row}>
            <button type="button" style={styles.primaryBtn} onClick={saveEdit} disabled={isSaving}>
              {isSaving ? "Saving..." : "Save"}
            </button>
            <button type="button" style={styles.secondaryBtn} onClick={() => setEditing(false)}>
              Cancel
            </button>
          </div>
          </>
        ) : (
          <>
          <div style={styles.head}>
            <h3 style={{ margin: 0 }}>{notice.title}</h3>
            {notice.isPinned ? <span style={styles.pillPinned}>Pinned</span> : null}
          </div>

          <p style={{ marginTop: 10 }}>{notice.content}</p>

          {notice.image ? (
            <img
              src={imageSrc}
              alt="notice"
              style={styles.image}
              loading="lazy"
              onClick={() => setIsImageOpen(true)}
            />
          ) : null}

          <p style={styles.metaLine}>
            <b>Category:</b> {notice.category || "General"}
          </p>
          <p style={styles.metaLine}>
            <b>Priority:</b> {notice.priority || "Low"}
          </p>

          {canManage ? (
            <div style={styles.row}>
              <button type="button" style={styles.secondaryBtn} onClick={togglePin}>
                {notice.isPinned ? "Unpin" : "Pin"}
              </button>
              <button type="button" style={styles.secondaryBtn} onClick={() => setEditing(true)}>
                Edit
              </button>
              <button type="button" style={styles.dangerBtn} onClick={removeNotice}>
                Delete
              </button>
            </div>
          ) : null}
          </>
        )}
      </div>

      {isImageOpen ? (
        <div
          style={styles.lightbox}
          onClick={(e) => {
            // Close only when clicking the backdrop, not the image container.
            if (e.target === e.currentTarget) setIsImageOpen(false)
          }}
          role="dialog"
          aria-modal="true"
        >
          <div style={styles.lightboxInner}>
            <button
              type="button"
              style={styles.lightboxClose}
              onClick={() => setIsImageOpen(false)}
              aria-label="Close image"
              title="Close (Esc)"
            >
              X
            </button>
            <img src={imageSrc} alt="notice" style={styles.lightboxImg} />
          </div>
        </div>
      ) : null}
    </>
  )
}

const styles = {
  card: {
    background: "white",
    padding: "15px",
    borderRadius: "10px",
    boxShadow: "0 3px 10px rgba(0,0,0,0.08)",
    border: "1px solid #e7eefb"
  },
  head: {
    display: "flex",
    alignItems: "center",
    justifyContent: "space-between",
    gap: "10px"
  },
  pillPinned: {
    background: "#ffecc6",
    color: "#885105",
    padding: "4px 10px",
    borderRadius: "999px",
    fontWeight: 700,
    fontSize: "0.8rem"
  },
  metaLine: {
    margin: "6px 0",
    color: "#334a6a"
  },
  row: {
    display: "flex",
    gap: "10px",
    flexWrap: "wrap",
    marginTop: "12px"
  },
  input: {
    width: "100%",
    padding: "10px",
    marginTop: "10px",
    borderRadius: "8px",
    border: "1px solid #d5deee"
  },
  textarea: {
    width: "100%",
    padding: "10px",
    height: "100px",
    marginTop: "10px",
    borderRadius: "8px",
    border: "1px solid #d5deee"
  },
  image: {
    width: "100%",
    marginTop: "10px",
    borderRadius: "10px",
    border: "1px solid #e7eefb",
    maxHeight: "320px",
    objectFit: "contain",
    background: "#f4f7ff",
    cursor: "pointer"
  },
  lightbox: {
    position: "fixed",
    inset: 0,
    background: "rgba(0,0,0,0.78)",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    padding: "20px",
    zIndex: 9999
  },
  lightboxInner: {
    width: "min(980px, 96vw)",
    maxHeight: "92vh",
    position: "relative"
  },
  lightboxImg: {
    width: "100%",
    maxHeight: "92vh",
    objectFit: "contain",
    borderRadius: "12px",
    background: "#0b1020"
  },
  lightboxClose: {
    position: "absolute",
    top: "-10px",
    right: "-10px",
    background: "rgba(255,255,255,0.92)",
    border: "1px solid rgba(255,255,255,0.6)",
    borderRadius: "999px",
    padding: "10px 12px",
    cursor: "pointer",
    fontWeight: 800,
    lineHeight: 1
  },
  primaryBtn: {
    padding: "10px 14px",
    background: "#0b69c7",
    border: "none",
    color: "white",
    borderRadius: "8px",
    cursor: "pointer"
  },
  secondaryBtn: {
    padding: "10px 14px",
    background: "#edf4ff",
    border: "1px solid #d2e3ff",
    color: "#1f4e8f",
    borderRadius: "8px",
    cursor: "pointer"
  },
  dangerBtn: {
    padding: "10px 14px",
    background: "#ffe8e8",
    border: "1px solid #ffd7d7",
    color: "#8a1811",
    borderRadius: "8px",
    cursor: "pointer"
  }
}

export default NoticeCard
