// import axios from "axios";

// const API = axios.create({
// baseURL:"http://localhost:5000/api"
// })

// export const getNotices = () => API.get("/notices/all")

// export const getProfile = (id) => API.get(`/users/profile/${id}`)

// export const updateProfile = (id,data) =>
// API.put(`/users/update/${id}`,data)

// export default API
import axios from "axios";

export const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || "";

const API = axios.create({
// If REACT_APP_API_BASE_URL is set, use it (prod). Otherwise use CRA dev proxy (/api).
baseURL: API_BASE_URL ? `${API_BASE_URL}/api` : "/api"
})

API.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

// AUTH
export const loginUser = (data)=>API.post("/auth/login",data)
export const registerUser = (data)=>API.post("/auth/register",data)


// NOTICES
export const getNotices = async () => {
  try {
    const res = await API.get("/notices");
    return { ...res, data: res.data?.data || [] };
  } catch (err) {
    if (err?.response?.status === 404) {
      // Backward compatibility with older backend route.
      const res = await API.get("/notices/all");
      return { ...res, data: res.data || [] };
    }
    throw err;
  }
};

export const createNotice = async (data) => {
  const isFormData = typeof FormData !== "undefined" && data instanceof FormData;
  const path = isFormData ? "/notices/create" : "/notices";

  try {
    return await API.post(path, data);
  } catch (err) {
    if (err?.response?.status === 404) {
      // Backward compatibility with older backend route.
      const fallbackPath = isFormData ? "/notices/create" : "/notices/create";
      return await API.post(fallbackPath, data);
    }
    throw err;
  }
};
export const deleteNotice = (id)=>API.delete(`/notices/${id}`)
export const updateNotice = async (id,data) => {
  try {
    return await API.put(`/notices/${id}`, data);
  } catch (err) {
    if (err?.response?.status === 404) {
      // Older server might expose a different update route.
      return await API.put(`/notices/update/${id}`, data);
    }
    throw err;
  }
};

export const setNoticePinned = async (id,isPinned) => {
  try {
    return await API.patch(`/notices/${id}/pin`, { isPinned });
  } catch (err) {
    if (err?.response?.status === 404) {
      // No pin endpoint on older server.
      return await API.put(`/notices/${id}`, { isPinned });
    }
    throw err;
  }
};


// USERS
export const getUsers = async () => {
  try {
    return await API.get("/users");
  } catch (err) {
    if (err?.response?.status === 404) {
      return await API.get("/users/all");
    }
    throw err;
  }
};

export const getStudents = async () => {
  try {
    return await API.get("/users/students");
  } catch (err) {
    if (err?.response?.status === 404) {
      // Avoid falling back to admin-only endpoints like /users or /users/all.
      // If /users/students doesn't exist, the caller should surface an error.
      throw new Error("Students endpoint not found: backend must expose GET /api/users/students");
    }
    throw err;
  }
};

export const getCoordinators = async () => {
  try {
    return await API.get("/users/coordinators");
  } catch (err) {
    if (err?.response?.status === 404) {
      // Avoid falling back to admin-only endpoints like /users or /users/all.
      // If /users/coordinators doesn't exist, the caller should surface an error.
      throw new Error("Coordinators endpoint not found: backend must expose GET /api/users/coordinators");
    }
    throw err;
  }
};
export const getProfile = (id)=>API.get(`/users/profile/${id}`)
export const updateProfile = (id,data)=>API.put(`/users/update/${id}`,data)


// COORDINATOR PERMISSIONS
export const makeCoordinator = (id)=>
API.put(`/users/make-coordinator/${id}`)

export const removeCoordinator = (id)=>
API.put(`/users/remove-coordinator/${id}`)

// ADMIN: manage users
export const deleteUser = (id)=>
API.delete(`/users/${id}`)


export default API
