// // // import React, { useCallback, useEffect, useMemo, useState } from "react";
// // // import api from "../utils/api";
// // // import NoticeCard from "./NoticeCard";

// // // const emptyNoticeForm = {
// // //   title: "",
// // //   content: "",
// // //   category: "",
// // //   priority: "Low",
// // //   expiryDate: ""
// // // };

// // // const emptyProfileForm = {
// // //   name: "",
// // //   email: "",
// // //   phoneNumber: "",
// // //   branch: "",
// // //   rollNumber: "",
// // //   currentPassword: "",
// // //   newPassword: "",
// // //   confirmPassword: ""
// // // };

// // // const normalizeAppRole = (role = "") => (role === "teacher" ? "faculty" : role);

// // // function Dashboard() {
// // //   const [currentUser, setCurrentUser] = useState(null);
// // //   const [notices, setNotices] = useState([]);
// // //   const [users, setUsers] = useState([]);
// // //   const [noticeForm, setNoticeForm] = useState(emptyNoticeForm);
// // //   const [profileForm, setProfileForm] = useState(emptyProfileForm);
// // //   const [studentQuery, setStudentQuery] = useState("");
// // //   const [studentNameToCheck, setStudentNameToCheck] = useState("");
// // //   const [checkedStudent, setCheckedStudent] = useState(null);
// // //   const [isCheckingStudent, setIsCheckingStudent] = useState(false);
// // //   const [dashboardTab, setDashboardTab] = useState("overview");
// // //   const [editingNoticeId, setEditingNoticeId] = useState("");
// // //   const [filters, setFilters] = useState({
// // //     q: "",
// // //     priority: "All",
// // //     category: "All",
// // //     sortBy: "newest",
// // //     activeOnly: true
// // //   });
// // //   const [categories, setCategories] = useState([]);
// // //   const [isLoadingNotices, setIsLoadingNotices] = useState(false);
// // //   const [isSavingNotice, setIsSavingNotice] = useState(false);
// // //   const [isSavingProfile, setIsSavingProfile] = useState(false);
// // //   const [error, setError] = useState("");
// // //   const [success, setSuccess] = useState("");

// // //   const role = normalizeAppRole(currentUser?.role);
// // //   const isAdmin = role === "admin";
// // //   const isFaculty = role === "faculty";
// // //   const isStudent = role === "student";

// // //   const canCreateNotice = useMemo(() => {
// // //     if (!currentUser) return false;
// // //     if (["admin", "faculty"].includes(role)) return true;
// // //     return role === "student" && currentUser.canPostNotices;
// // //   }, [currentUser, role]);

// // //   const studentStats = useMemo(() => {
// // //     const highPriority = notices.filter((n) => n.priority === "High").length;
// // //     const expiringSoon = notices.filter((n) => {
// // //       if (!n.expiryDate) return false;
// // //       const diff = new Date(n.expiryDate).getTime() - Date.now();
// // //       return diff > 0 && diff <= 3 * 24 * 60 * 60 * 1000;
// // //     }).length;

// // //     return {
// // //       total: notices.length,
// // //       highPriority,
// // //       expiringSoon
// // //     };
// // //   }, [notices]);

// // //   const dashboardTabs = useMemo(() => {
// // //     if (!currentUser) return [];

// // //     if (isAdmin) {
// // //       return [
// // //         { key: "overview", label: "Overview" },
// // //         { key: "users", label: "User Control" },
// // //         { key: "post", label: "Post Notice" },
// // //         { key: "notices", label: "Notices" },
// // //         { key: "profile", label: "My Profile" }
// // //       ];
// // //     }

// // //     if (isFaculty) {
// // //       return [
// // //         { key: "overview", label: "Overview" },
// // //         { key: "users", label: "Student Rights" },
// // //         { key: "post", label: "Post Notice" },
// // //         { key: "notices", label: "Notices" },
// // //         { key: "profile", label: "My Profile" }
// // //       ];
// // //     }

// // //     if (canCreateNotice) {
// // //       return [
// // //         { key: "overview", label: "Overview" },
// // //         { key: "post", label: "Post Notice" },
// // //         { key: "notices", label: "Notices" },
// // //         { key: "profile", label: "My Profile" }
// // //       ];
// // //     }

// // //     return [
// // //       { key: "overview", label: "Overview" },
// // //       { key: "notices", label: "Notices" },
// // //       { key: "profile", label: "My Profile" }
// // //     ];
// // //   }, [canCreateNotice, currentUser, isAdmin, isFaculty]);

// // //   const roleStats = useMemo(() => {
// // //     const mine = notices.filter((n) => n.createdBy?._id === currentUser?.id).length;
// // //     return {
// // //       totalNotices: notices.length,
// // //       myNotices: mine,
// // //       categories: categories.length,
// // //       users: users.length
// // //     };
// // //   }, [categories.length, currentUser?.id, notices, users.length]);

// // //   const filteredUsers = useMemo(() => {
// // //     if (!studentQuery.trim()) return users;
// // //     const q = studentQuery.trim().toLowerCase();
// // //     return users.filter((u) =>
// // //       [u.name, u.email, u.rollNumber, u.branch, u.phoneNumber]
// // //         .filter(Boolean)
// // //         .some((value) => value.toLowerCase().includes(q))
// // //     );
// // //   }, [studentQuery, users]);

// // //   const loadCurrentUser = useCallback(async () => {
// // //     try {
// // //       const res = await api.get("/auth/me");
// // //       const user = res.data.user;
// // //       setCurrentUser(user);
// // //       setDashboardTab(user.role === "admin" ? "overview" : "overview");
// // //       setProfileForm((prev) => ({
// // //         ...prev,
// // //         name: user.name || "",
// // //         email: user.email || "",
// // //         phoneNumber: user.phoneNumber || "",
// // //         branch: user.branch || "",
// // //         rollNumber: user.rollNumber || ""
// // //       }));

// // //       localStorage.setItem("name", user.name);
// // //       localStorage.setItem("role", normalizeAppRole(user.role));
// // //       localStorage.setItem("canPostNotices", String(user.canPostNotices));
// // //     } catch (err) {
// // //       setError("Session expired. Please login again.");
// // //       localStorage.removeItem("token");
// // //       window.location.replace("/login");
// // //     }
// // //   }, []);

// // //   const loadNotices = useCallback(async () => {
// // //     try {
// // //       setIsLoadingNotices(true);
// // //       setError("");

// // //       const res = await api.get("/notices", {
// // //         params: {
// // //           ...filters,
// // //           activeOnly: filters.activeOnly ? "true" : "false"
// // //         }
// // //       });

// // //       const fetchedNotices = Array.isArray(res.data) ? res.data : res.data.data;
// // //       setNotices(fetchedNotices || []);
// // //       setCategories([...new Set((fetchedNotices || []).map((n) => n.category).filter(Boolean))]);
// // //     } catch (err) {
// // //       setError(err.response?.data?.message || "Failed to load notices");
// // //     } finally {
// // //       setIsLoadingNotices(false);
// // //     }
// // //   }, [filters]);

// // //   const loadUsers = useCallback(async () => {
// // //     if (!isAdmin && !isFaculty) return;

// // //     try {
// // //       const res = isAdmin ? await api.get("/users") : await api.get("/users/students");
// // //       setUsers(res.data || []);
// // //     } catch (err) {
// // //       setError(err.response?.data?.message || "Failed to load users");
// // //     }
// // //   }, [isAdmin, isFaculty]);

// // //   useEffect(() => {
// // //     loadCurrentUser();
// // //   }, [loadCurrentUser]);

// // //   useEffect(() => {
// // //     if (currentUser) {
// // //       loadNotices();
// // //     }
// // //   }, [currentUser, loadNotices]);

// // //   useEffect(() => {
// // //     loadUsers();
// // //   }, [loadUsers]);

// // //   const onFilterChange = (key, value) => {
// // //     setFilters((prev) => ({ ...prev, [key]: value }));
// // //   };

// // //   const onNoticeFormChange = (e) => {
// // //     setNoticeForm((prev) => ({
// // //       ...prev,
// // //       [e.target.name]: e.target.value
// // //     }));
// // //   };

// // //   const onProfileFormChange = (e) => {
// // //     setProfileForm((prev) => ({
// // //       ...prev,
// // //       [e.target.name]: e.target.value
// // //     }));
// // //   };

// // //   const resetNoticeForm = () => {
// // //     setNoticeForm(emptyNoticeForm);
// // //     setEditingNoticeId("");
// // //   };

// // //   const submitNotice = async (e) => {
// // //     e.preventDefault();
// // //     setError("");
// // //     setSuccess("");

// // //     if (!canCreateNotice) {
// // //       setError("You do not have permission to post notices.");
// // //       return;
// // //     }

// // //     if (!noticeForm.title || !noticeForm.content) {
// // //       setError("Title and content are required.");
// // //       return;
// // //     }

// // //     try {
// // //       setIsSavingNotice(true);
// // //       const payload = {
// // //         ...noticeForm,
// // //         isPinned: Boolean(noticeForm.isPinned),
// // //         expiryDate: noticeForm.expiryDate || null
// // //       };

// // //       if (editingNoticeId) {
// // //         await api.put(`/notices/${editingNoticeId}`, payload);
// // //         setSuccess("Notice updated.");
// // //       } else {
// // //         await api.post("/notices", payload);
// // //         setSuccess("Notice posted.");
// // //       }

// // //       resetNoticeForm();
// // //       await loadNotices();
// // //       setDashboardTab("notices");
// // //       setFilters((prev) => ({ ...prev, q: "", category: "All" }));
// // //     } catch (err) {
// // //       setError(err.response?.data?.message || "Failed to save notice");
// // //     } finally {
// // //       setIsSavingNotice(false);
// // //     }
// // //   };

// // //   const submitProfileUpdate = async (e) => {
// // //     e.preventDefault();
// // //     setError("");
// // //     setSuccess("");

// // //     if (!profileForm.name || !profileForm.email) {
// // //       setError("Name and email are required.");
// // //       return;
// // //     }

// // //     if (profileForm.newPassword && profileForm.newPassword !== profileForm.confirmPassword) {
// // //       setError("New password and confirm password must match.");
// // //       return;
// // //     }

// // //     try {
// // //       setIsSavingProfile(true);

// // //       const payload = {
// // //         name: profileForm.name,
// // //         email: profileForm.email,
// // //         phoneNumber: profileForm.phoneNumber
// // //       };

// // //       if (isStudent) {
// // //         payload.branch = profileForm.branch;
// // //         payload.rollNumber = profileForm.rollNumber;
// // //       }

// // //       if (profileForm.newPassword) {
// // //         payload.currentPassword = profileForm.currentPassword;
// // //         payload.newPassword = profileForm.newPassword;
// // //       }

// // //       const res = await api.patch("/auth/me", payload);
// // //       setCurrentUser(res.data.user);
// // //       setProfileForm((prev) => ({
// // //         ...prev,
// // //         currentPassword: "",
// // //         newPassword: "",
// // //         confirmPassword: ""
// // //       }));

// // //       localStorage.setItem("name", res.data.user.name);
// // //       localStorage.setItem("role", normalizeAppRole(res.data.user.role));
// // //       localStorage.setItem("canPostNotices", String(res.data.user.canPostNotices));
// // //       setSuccess("Profile updated successfully.");
// // //     } catch (err) {
// // //       setError(err.response?.data?.message || "Failed to update profile");
// // //     } finally {
// // //       setIsSavingProfile(false);
// // //     }
// // //   };

// // //   const handleDeleteNotice = async (noticeId) => {
// // //     setError("");
// // //     setSuccess("");
// // //     if (!window.confirm("Delete this notice?")) return;

// // //     try {
// // //       await api.delete(`/notices/${noticeId}`);
// // //       setSuccess("Notice deleted.");
// // //       await loadNotices();
// // //     } catch (err) {
// // //       setError(err.response?.data?.message || "Failed to delete notice");
// // //     }
// // //   };

// // //   const handleTogglePinNotice = async (notice) => {
// // //     try {
// // //       setError("");
// // //       setSuccess("");
// // //       await api.patch(`/notices/${notice._id}/pin`, { isPinned: !notice.isPinned });
// // //       setSuccess(notice.isPinned ? "Notice unpinned." : "Notice pinned.");
// // //       await loadNotices();
// // //     } catch (err) {
// // //       setError(err.response?.data?.message || "Failed to update pin status");
// // //     }
// // //   };

// // //   const handleStartEdit = (notice) => {
// // //     setEditingNoticeId(notice._id);
// // //     setNoticeForm({
// // //       title: notice.title || "",
// // //       content: notice.content || "",
// // //       category: notice.category || "",
// // //       priority: notice.priority || "Low",
// // //       expiryDate: notice.expiryDate ? new Date(notice.expiryDate).toISOString().slice(0, 10) : ""
// // //     });
// // //   };

// // //   const handleUserAccessUpdate = async (userId, payload) => {
// // //     try {
// // //       await api.patch(`/users/${userId}/access`, payload);
// // //       await loadUsers();
// // //       await loadNotices();
// // //       setSuccess("User access updated.");
// // //     } catch (err) {
// // //       setError(err.response?.data?.message || "Failed to update user access");
// // //     }
// // //   };

// // //   const handleStudentPostingRights = async (userId, canPostNotices) => {
// // //     try {
// // //       await api.patch(`/users/${userId}/posting-rights`, { canPostNotices });
// // //       await loadUsers();
// // //       setSuccess("Student posting rights updated.");
// // //     } catch (err) {
// // //       setError(err.response?.data?.message || "Failed to update posting rights");
// // //     }
// // //   };

// // //   const canEditNotice = (notice) =>
// // //     Boolean(
// // //       currentUser
// // //       && (
// // //         currentUser.role === "admin"
// // //         || ["teacher", "faculty"].includes(currentUser.role)
// // //         || notice.createdBy?._id === currentUser.id
// // //       )
// // //     );
// // //   const canPinNotice = (notice) =>
// // //     Boolean(
// // //       currentUser
// // //       && (
// // //         currentUser.role === "admin"
// // //         || ["teacher", "faculty"].includes(currentUser.role)
// // //         || notice.createdBy?._id === currentUser.id
// // //       )
// // //     );

// // //   const checkStudentByName = async () => {
// // //     const name = studentNameToCheck.trim();
// // //     if (!name) {
// // //       setError("Enter student name to check.");
// // //       return;
// // //     }

// // //     try {
// // //       setIsCheckingStudent(true);
// // //       setError("");
// // //       setCheckedStudent(null);
// // //       const res = await api.get("/users/students/find", { params: { name } });
// // //       setCheckedStudent(res.data);
// // //       setSuccess("Student found.");
// // //     } catch (err) {
// // //       setCheckedStudent(null);
// // //       setError(err.response?.data?.message || "Student not found");
// // //     } finally {
// // //       setIsCheckingStudent(false);
// // //     }
// // //   };

// // //   const grantAccessToCheckedStudent = async () => {
// // //     if (!checkedStudent?._id) return;
// // //     await handleStudentPostingRights(checkedStudent._id, true);
// // //     setCheckedStudent((prev) => (prev ? { ...prev, canPostNotices: true } : prev));
// // //   };

// // //   if (!currentUser) {
// // //     return (
// // //       <div className="page-shell">
// // //         <section className="card">
// // //           <p className="muted-text">Loading dashboard...</p>
// // //         </section>
// // //       </div>
// // //     );
// // //   }

// // //   return (
// // //     <div className="page-shell">
// // //       <section className="card dashboard-card">
// // //         <div className="dashboard-top">
// // //           <div>
// // //             <h2>{role.toUpperCase()} Dashboard</h2>
// // //             <p className="muted-text">
// // //               {isStudent && !currentUser.canPostNotices
// // //                 ? "Student access: personalized notice view + profile management"
// // //                 : "You can view and manage notices based on your permissions"}
// // //             </p>
// // //           </div>
// // //           <button className="secondary-btn" onClick={loadNotices} disabled={isLoadingNotices}>
// // //             Refresh
// // //           </button>
// // //         </div>

// // //         <div className="tab-row">
// // //           {dashboardTabs.map((tab) => (
// // //             <button
// // //               key={tab.key}
// // //               className={`tab-btn ${dashboardTab === tab.key ? "tab-active" : ""}`}
// // //               onClick={() => setDashboardTab(tab.key)}
// // //             >
// // //               {tab.label}
// // //             </button>
// // //           ))}
// // //         </div>

// // //         {error ? <p className="error-text">{error}</p> : null}
// // //         {success ? <p className="success-text">{success}</p> : null}
// // //       </section>

// // //       {dashboardTab === "overview" ? (
// // //         <section className="card">
// // //           <h3>{isStudent ? "Student Snapshot" : "Dashboard Snapshot"}</h3>
// // //           <div className="stats-grid">
// // //             <article className="stat-card">
// // //               <h4>Total Active Notices</h4>
// // //               <p>{roleStats.totalNotices}</p>
// // //             </article>
// // //             <article className="stat-card">
// // //               <h4>High Priority</h4>
// // //               <p>{studentStats.highPriority}</p>
// // //             </article>
// // //             <article className="stat-card">
// // //               <h4>Expiring in 3 Days</h4>
// // //               <p>{studentStats.expiringSoon}</p>
// // //             </article>
// // //             {!isStudent ? (
// // //               <article className="stat-card">
// // //                 <h4>My Notices</h4>
// // //                 <p>{roleStats.myNotices}</p>
// // //               </article>
// // //             ) : null}
// // //             {isAdmin ? (
// // //               <article className="stat-card">
// // //                 <h4>Total Users</h4>
// // //                 <p>{roleStats.users}</p>
// // //               </article>
// // //             ) : null}
// // //             <article className="stat-card">
// // //               <h4>Categories</h4>
// // //               <p>{roleStats.categories}</p>
// // //             </article>
// // //           </div>

// // //           <div className="quick-action-row">
// // //             {canCreateNotice ? (
// // //               <button className="secondary-btn inline-btn" onClick={() => setDashboardTab("post")}>
// // //                 Create Notice
// // //               </button>
// // //             ) : null}
// // //             <button className="secondary-btn inline-btn" onClick={() => setDashboardTab("notices")}>
// // //               Browse Notices
// // //             </button>
// // //             <button className="secondary-btn inline-btn" onClick={() => setDashboardTab("profile")}>
// // //               Edit Profile
// // //             </button>
// // //             {isAdmin ? (
// // //               <button className="secondary-btn inline-btn" onClick={() => setDashboardTab("users")}>
// // //                 Manage Users
// // //               </button>
// // //             ) : null}
// // //           </div>
// // //         </section>
// // //       ) : null}

// // //       {dashboardTab === "profile" ? (
// // //         <section className="card">
// // //           <h3>My Profile</h3>
// // //           <div className="profile-view-card">
// // //             <h4>Profile Overview</h4>
// // //             <p><strong>Name:</strong> {currentUser.name}</p>
// // //             <p><strong>Email:</strong> {currentUser.email}</p>
// // //             <p><strong>Phone:</strong> {currentUser.phoneNumber || "Not set"}</p>
// // //             <p><strong>Role:</strong> {role}</p>
// // //             {isStudent ? <p><strong>Branch:</strong> {currentUser.branch || "Not set"}</p> : null}
// // //             {isStudent ? <p><strong>Roll Number:</strong> {currentUser.rollNumber || "Not set"}</p> : null}
// // //             <p>
// // //               <strong>Posting Rights:</strong> {canCreateNotice ? "Enabled" : "View Only"}
// // //             </p>
// // //           </div>

// // //           <h4 style={{ marginTop: "14px" }}>Edit Profile</h4>
// // //           <form onSubmit={submitProfileUpdate}>
// // //             <div className="filter-grid">
// // //               <div>
// // //                 <label htmlFor="name">Name</label>
// // //                 <input
// // //                   id="name"
// // //                   name="name"
// // //                   type="text"
// // //                   value={profileForm.name}
// // //                   onChange={onProfileFormChange}
// // //                 />
// // //               </div>
// // //               <div>
// // //                 <label htmlFor="email">Email</label>
// // //                 <input
// // //                   id="email"
// // //                   name="email"
// // //                   type="email"
// // //                   value={profileForm.email}
// // //                   onChange={onProfileFormChange}
// // //                 />
// // //               </div>
// // //               <div>
// // //                 <label htmlFor="phoneNumber">Phone Number</label>
// // //                 <input
// // //                   id="phoneNumber"
// // //                   name="phoneNumber"
// // //                   type="tel"
// // //                   value={profileForm.phoneNumber}
// // //                   onChange={onProfileFormChange}
// // //                 />
// // //               </div>
// // //               <div>
// // //                 <label htmlFor="currentPassword">Current Password</label>
// // //                 <input
// // //                   id="currentPassword"
// // //                   name="currentPassword"
// // //                   type="password"
// // //                   value={profileForm.currentPassword}
// // //                   onChange={onProfileFormChange}
// // //                   placeholder="Required only for password change"
// // //                 />
// // //               </div>
// // //               <div>
// // //                 <label htmlFor="newPassword">New Password</label>
// // //                 <input
// // //                   id="newPassword"
// // //                   name="newPassword"
// // //                   type="password"
// // //                   value={profileForm.newPassword}
// // //                   onChange={onProfileFormChange}
// // //                 />
// // //               </div>
// // //               {isStudent ? (
// // //                 <>
// // //                   <div>
// // //                     <label htmlFor="branch">Branch</label>
// // //                     <input
// // //                       id="branch"
// // //                       name="branch"
// // //                       type="text"
// // //                       value={profileForm.branch}
// // //                       onChange={onProfileFormChange}
// // //                     />
// // //                   </div>
// // //                   <div>
// // //                     <label htmlFor="rollNumber">Roll Number</label>
// // //                     <input
// // //                       id="rollNumber"
// // //                       name="rollNumber"
// // //                       type="text"
// // //                       value={profileForm.rollNumber}
// // //                       onChange={onProfileFormChange}
// // //                     />
// // //                   </div>
// // //                 </>
// // //               ) : null}
// // //             </div>
// // //             <label htmlFor="confirmPassword">Confirm New Password</label>
// // //             <input
// // //               id="confirmPassword"
// // //               name="confirmPassword"
// // //               type="password"
// // //               value={profileForm.confirmPassword}
// // //               onChange={onProfileFormChange}
// // //             />

// // //             <button className="primary-btn inline-btn" type="submit" disabled={isSavingProfile}>
// // //               {isSavingProfile ? "Saving..." : "Update Profile"}
// // //             </button>
// // //           </form>
// // //         </section>
// // //       ) : null}

// // //       {canCreateNotice && dashboardTab === "post" ? (
// // //         <section className="card">
// // //           <h3>{editingNoticeId ? "Edit Notice" : "Post Notice / Update"}</h3>
// // //           <form onSubmit={submitNotice}>
// // //             <div className="filter-grid">
// // //               <input
// // //                 name="title"
// // //                 type="text"
// // //                 placeholder="Notice title"
// // //                 value={noticeForm.title}
// // //                 onChange={onNoticeFormChange}
// // //               />
// // //               <input
// // //                 name="category"
// // //                 type="text"
// // //                 placeholder="Category"
// // //                 value={noticeForm.category}
// // //                 onChange={onNoticeFormChange}
// // //               />
// // //               <select name="priority" value={noticeForm.priority} onChange={onNoticeFormChange}>
// // //                 <option value="Low">Low</option>
// // //                 <option value="Medium">Medium</option>
// // //                 <option value="High">High</option>
// // //               </select>
// // //               <div>
// // //                 <label htmlFor="expiryDate">Expiry Date (pick from calendar)</label>
// // //                 <input
// // //                   id="expiryDate"
// // //                   name="expiryDate"
// // //                   type="date"
// // //                   value={noticeForm.expiryDate}
// // //                   onChange={onNoticeFormChange}
// // //                 />
// // //               </div>
// // //             </div>

// // //             <label htmlFor="content">Content</label>
// // //             <textarea
// // //               id="content"
// // //               name="content"
// // //               value={noticeForm.content}
// // //               onChange={onNoticeFormChange}
// // //               placeholder="Write notice details"
// // //             />

// // //             <div className="action-row">
// // //               <button className="primary-btn inline-btn" type="submit" disabled={isSavingNotice}>
// // //                 {isSavingNotice ? "Saving..." : editingNoticeId ? "Update Notice" : "Post Notice"}
// // //               </button>
// // //               {editingNoticeId ? (
// // //                 <button className="secondary-btn inline-btn" type="button" onClick={resetNoticeForm}>
// // //                   Cancel Edit
// // //                 </button>
// // //               ) : null}
// // //             </div>
// // //           </form>
// // //         </section>
// // //       ) : null}

// // //       {(isAdmin || isFaculty) && dashboardTab === "users" ? (
// // //         <section className="card">
// // //           <h3>{isAdmin ? "Admin User Management" : "Faculty Student Rights"}</h3>
// // //           <p className="muted-text">
// // //             {isAdmin
// // //               ? "Manage roles and grant or revoke posting rights for student coordinators."
// // //               : "Pick students and grant/revoke rights to post notices as coordinators."}
// // //           </p>
// // //           <div className="action-row">
// // //             <input
// // //               type="text"
// // //               placeholder="Enter exact student name"
// // //               value={studentNameToCheck}
// // //               onChange={(e) => setStudentNameToCheck(e.target.value)}
// // //             />
// // //             <button type="button" className="secondary-btn inline-btn" onClick={checkStudentByName} disabled={isCheckingStudent}>
// // //               {isCheckingStudent ? "Checking..." : "Check Student"}
// // //             </button>
// // //           </div>

// // //           {checkedStudent ? (
// // //             <article className="user-card">
// // //               <h4>{checkedStudent.name}</h4>
// // //               <p>{checkedStudent.email}</p>
// // //               <p>Phone: {checkedStudent.phoneNumber || "N/A"}</p>
// // //               <p>Branch: {checkedStudent.branch || "N/A"}</p>
// // //               <p>Roll Number: {checkedStudent.rollNumber || "N/A"}</p>
// // //               <p>Can Post: {checkedStudent.canPostNotices ? "Yes" : "No"}</p>
// // //               {!checkedStudent.canPostNotices ? (
// // //                 <button type="button" className="secondary-btn" onClick={grantAccessToCheckedStudent}>
// // //                   Grant Access
// // //                 </button>
// // //               ) : null}
// // //             </article>
// // //           ) : null}

// // //           <input
// // //             type="text"
// // //             placeholder="Search student by name/email/roll/branch/phone"
// // //             value={studentQuery}
// // //             onChange={(e) => setStudentQuery(e.target.value)}
// // //           />
// // //           <div className="user-grid">
// // //             {filteredUsers.map((user) => (
// // //               <article className="user-card" key={user._id}>
// // //                 <h4>{user.name}</h4>
// // //                 <p>{user.email}</p>
// // //                 <p>Role: {normalizeAppRole(user.role)}</p>
// // //                 <p>Phone: {user.phoneNumber || "N/A"}</p>
// // //                 <p>Branch: {user.branch || "N/A"}</p>
// // //                 <p>Roll Number: {user.rollNumber || "N/A"}</p>
// // //                 <p>Can Post: {user.canPostNotices ? "Yes" : "No"}</p>

// // //                 {isAdmin ? (
// // //                   <>
// // //                     <label>Role</label>
// // //                     <select
// // //                       value={normalizeAppRole(user.role)}
// // //                       onChange={(e) => handleUserAccessUpdate(user._id, { role: e.target.value })}
// // //                     >
// // //                       <option value="student">Student</option>
// // //                       <option value="faculty">Faculty</option>
// // //                       <option value="admin">Admin</option>
// // //                     </select>
// // //                   </>
// // //                 ) : null}

// // //                 {normalizeAppRole(user.role) === "student" ? (
// // //                   <button
// // //                     className="secondary-btn"
// // //                     onClick={() => handleStudentPostingRights(user._id, !user.canPostNotices)}
// // //                   >
// // //                     {user.canPostNotices ? "Revoke Coordinator Rights" : "Grant Coordinator Rights"}
// // //                   </button>
// // //                 ) : null}
// // //               </article>
// // //             ))}
// // //           </div>
// // //         </section>
// // //       ) : null}

// // //       {dashboardTab === "notices" ? (
// // //         <section className="card">
// // //           <h3>Notices</h3>
// // //           <div className="filter-grid">
// // //             <input
// // //               type="text"
// // //               placeholder="Search by title, content, category"
// // //               value={filters.q}
// // //               onChange={(e) => onFilterChange("q", e.target.value)}
// // //             />

// // //             <select value={filters.priority} onChange={(e) => onFilterChange("priority", e.target.value)}>
// // //               <option value="All">All Priorities</option>
// // //               <option value="High">High</option>
// // //               <option value="Medium">Medium</option>
// // //               <option value="Low">Low</option>
// // //             </select>

// // //             <select value={filters.category} onChange={(e) => onFilterChange("category", e.target.value)}>
// // //               <option value="All">All Categories</option>
// // //               {categories.map((category) => (
// // //                 <option key={category} value={category}>
// // //                   {category}
// // //                 </option>
// // //               ))}
// // //             </select>

// // //             <select value={filters.sortBy} onChange={(e) => onFilterChange("sortBy", e.target.value)}>
// // //               <option value="newest">Newest First</option>
// // //               <option value="oldest">Oldest First</option>
// // //               <option value="priority">By Priority</option>
// // //               <option value="expiry">By Expiry Date</option>
// // //             </select>
// // //           </div>

// // //           <label className="checkbox-wrap">
// // //             <input
// // //               type="checkbox"
// // //               checked={filters.activeOnly}
// // //               onChange={(e) => onFilterChange("activeOnly", e.target.checked)}
// // //             />
// // //             Show only active (not expired) notices
// // //           </label>

// // //           {isLoadingNotices ? <p className="muted-text">Loading notices...</p> : null}
// // //           {!isLoadingNotices && notices.length === 0 ? (
// // //             <p className="muted-text">No notices found for selected filters.</p>
// // //           ) : null}

// // //           <div className="notice-list">
// // //             {notices.map((notice) => (
// // //             <NoticeCard
// // //               key={notice._id}
// // //               notice={notice}
// // //               canEdit={canEditNotice(notice)}
// // //               canDelete={canEditNotice(notice)}
// // //               canPin={canPinNotice(notice)}
// // //               onTogglePin={() => handleTogglePinNotice(notice)}
// // //               onEdit={() => handleStartEdit(notice)}
// // //               onDelete={() => handleDeleteNotice(notice._id)}
// // //             />
// // //             ))}
// // //           </div>
// // //         </section>
// // //       ) : null}
// // //     </div>
// // //   );
// // // }

// // // export default Dashboard;
// // import {useEffect,useState} from "react";
// // import axios from "axios";

// // import NoticeCard from "./NoticeCard";
// // import Navbar from "./Navbar";

// // function Dashboard(){

// // const [notices,setNotices] = useState([]);

// // useEffect(()=>{

// // axios.get("http://localhost:5000/api/notices/all")
// // .then(res=>setNotices(res.data));

// // },[]);

// // return(

// // <div>

// // <Navbar/>

// // <h2>Recent Notices</h2>

// // <marquee>

// // {notices.map(n => n.title + " | ")}

// // </marquee>

// // {notices.map(n => (

// // <NoticeCard notice={n}/>

// // ))}

// // </div>

// // );

// // }

// // export default Dashboard;

// import {useEffect,useState} from "react";
// import axios from "axios";

// import Navbar from "../../components/Navbar/Navbar";
// import NoticeCard from "../../components/Notice/NoticeCard";
// import NoticeTicker from "../../components/Notice/NoticeTicker";

// function AdminDashboard(){

// const [notices,setNotices] = useState([]);
// const [search,setSearch] = useState("");
// const [category,setCategory] = useState("all");

// useEffect(()=>{

// fetchNotices();

// },[]);

// const fetchNotices = async()=>{

// const res = await axios.get(
// "http://localhost:5000/api/notices/all"
// );

// setNotices(res.data);

// };

// const filteredNotices = notices.filter(n => {

// const matchSearch =
// n.title.toLowerCase().includes(search.toLowerCase());

// const matchCategory =
// category==="all" || n.category===category;

// return matchSearch && matchCategory;

// });

// return(

// <div>

// <Navbar/>

// <NoticeTicker notices={notices}/>

// <div style={styles.container}>

// <h2>Admin Dashboard</h2>

// <div style={styles.filters}>

// <input
// placeholder="Search notices..."
// style={styles.search}
// onChange={(e)=>setSearch(e.target.value)}
// />

// <select
// style={styles.select}
// onChange={(e)=>setCategory(e.target.value)}
// >

// <option value="all">All</option>
// <option value="Events">Events</option>
// <option value="Hackathons">Hackathons</option>
// <option value="Holidays">Holidays</option>
// <option value="General">General</option>

// </select>

// </div>

// <div style={styles.grid}>

// {filteredNotices.map(n => (

// <NoticeCard key={n._id} notice={n}/>

// ))}

// </div>

// </div>

// </div>

// );

// }

// const styles = {

// container:{
// padding:"40px"
// },

// filters:{
// display:"flex",
// gap:"20px",
// marginBottom:"20px"
// },

// search:{
// padding:"10px",
// width:"250px",
// borderRadius:"6px",
// border:"1px solid #ccc"
// },

// select:{
// padding:"10px",
// borderRadius:"6px"
// },

// grid:{
// display:"grid",
// gridTemplateColumns:"repeat(auto-fill,minmax(250px,1fr))",
// gap:"20px"
// }

// };

// export default AdminDashboard;
import { useNavigate } from "react-router-dom"
import Navbar from "../../components/Navbar/Navbar"
import "./AdminDashboard.css"

function AdminDashboard(){

const navigate = useNavigate()

return(

<div>

<Navbar/>

<div className="admin-container">

<h2 className="admin-title">
Admin Dashboard
</h2>

<div className="admin-cards">

<div 
className="admin-card"
onClick={()=>navigate("/admin/post-notice")}
>
📢
<h3>Post Notice</h3>
<p>Create a new notice</p>
</div>

<div 
className="admin-card"
onClick={()=>navigate("/admin/manage-notices")}
>
📋
<h3>Manage Notices</h3>
<p>Edit or delete notices</p>
</div>

<div 
className="admin-card"
onClick={()=>navigate("/manage-users")}
>
👥
<h3>Manage Users</h3>
<p>View and control users</p>
</div>

<div 
className="admin-card"
onClick={()=>navigate("/profile")}
>
👤
<h3>My Profile</h3>
<p>Update your details</p>
</div>

</div>

</div>

</div>

)

}

export default AdminDashboard
