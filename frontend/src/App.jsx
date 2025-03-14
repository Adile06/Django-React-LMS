import { useState, useEffect } from "react";
import { Route, Routes, BrowserRouter } from "react-router-dom";

import { CartContext, ProfileContext } from "./views/plugin/Context";
import apiInstance from "./utils/axios";
import CartId from "./views/plugin/CartId";

import MainWrapper from "./layouts/MainWrapper";
import PrivateRoute from "./layouts/PrivateRoute";

import Register from "../src/views/auth/Register";
import Login from "../src/views/auth/Login";
import Logout from "./views/auth/Logout";
import ForgotPassword from "./views/auth/ForgotPassword";
import CreateNewPassword from "./views/auth/CreateNewPassword";

import Index from "./views/base/Index";
import ESKEPIndex from "./views/base/ESKEPIndex";
import ESKEPStudent from "./views/ESKEPstudent/Dashboard";
import OdevCreate from "./views/ESKEPstajer/OdevCreate";
import KitapTahliliCreate from "./views/ESKEPstajer/KitapTahliliCreate";
import DersSonuRaporuCreate from "./views/ESKEPstajer/DersSonuRaporuCreate";
import DersSonuAnketi from "./views/ESKEPstudent/DersSonuAnketi";
import CourseDetail from "./views/base/CourseDetail";
import Cart from "./views/base/Cart";
import Checkout from "./views/base/Checkout";
import Success from "./views/base/Success";
import Search from "./views/base/Search";

import HafizBilgiList from "./views/hafizbilgi/HafizBilgiList";
import StudentDashboard from "./views/student/Dashboard";
import StudentCourses from "./views/student/Courses";
import StudentCourseDetail from "./views/student/CourseDetail";
import Wishlist from "./views/student/Wishlist";
import StudentProfile from "./views/student/Profile";

import useAxios from "./utils/useAxios";
import UserData from "./views/plugin/UserData";
import StudentChangePassword from "./views/student/ChangePassword";

import AgentHafizBilgiList from "./views/agent/HafizBilgiList";
import AgentDashboard from "./views/agent/Dashboard";

import OrganizationChart from "./views/admin/OrganizationChart";

import CrudTableDeneme from "./views/CrudTable/CrudTableDeneme";

import Dashboard from "./views/instructor/Dashboard";
import Courses from "./views/instructor/Courses";
import Review from "./views/instructor/Review";
import Students from "./views/instructor/Students";
import Earning from "./views/instructor/Earning";
import Orders from "./views/instructor/Orders";
import Coupon from "./views/instructor/Coupon";
import TeacherNotification from "./views/instructor/TeacherNotification";
import QA from "./views/instructor/QA";
import ChangePassword from "./views/instructor/ChangePassword";
import Profile from "./views/instructor/Profile";
import CourseCreate from "./views/instructor/CourseCreate";

import HafizBilgiCreate from "./views/hafizbilgi/HafizBilgiCreate";
import CourseEdit from "./views/instructor/CourseEdit";
import ESKEPstajerOdevs from "./views/ESKEPstajer/Odevs";
import ESKEPinstructorOdevs from "./views/ESKEPinstructor/Odevs";
import ESKEPinstructorOdevDetail from "./views/ESKEPinstructor/OdevDetail";

function App() {
  const [cartCount, setCartCount] = useState(0);
  const [profile, setProfile] = useState([]);

  useEffect(() => {
    apiInstance.get(`course/cart-list/${CartId()}/`).then((res) => {
      setCartCount(res.data?.length);
    });

    useAxios()
      .get(`user/profile/${UserData()?.user_id}/`)
      .then((res) => {
        setProfile(res.data);
      });
  }, []);

  return (
    <CartContext.Provider value={[cartCount, setCartCount]}>
      <ProfileContext.Provider value={[profile, setProfile]}>
        <BrowserRouter>
          <MainWrapper>
            <Routes>
              <Route path="/register/" element={<Register />} />
              <Route path="/login/" element={<Login />} />
              <Route path="/logout/" element={<Logout />} />
              <Route path="/forgot-password/" element={<ForgotPassword />} />
              <Route
                path="/create-new-password/"
                element={<CreateNewPassword />}
              />

              {/* Base Routes */}
              <Route path="/" element={<Index />} />
              <Route path="/course-detail/:slug/" element={<CourseDetail />} />
              <Route path="/cart/" element={<Cart />} />
              <Route path="/checkout/:order_oid/" element={<Checkout />} />
              <Route
                path="/payment-success/:order_oid/"
                element={<Success />}
              />
              <Route path="/search/" element={<Search />} />

              {/* Hafız Bilgi Routes */}
              <Route path="/hafizbilgi/list/" element={<HafizBilgiList />} />
              <Route
                path="/hafizbilgi/create-hafizbilgi/"
                element={<HafizBilgiCreate />}
              />
              {/* ESKEP Routes */}
              <Route path="/eskep/" element={<ESKEPIndex />} />
              <Route path="/eskep/create-odev/" element={<OdevCreate />} />
              <Route path="/eskep/create-kitaptahlili/" element={<KitapTahliliCreate />} />
              <Route path="/eskep/create-derssonuraporu/" element={<DersSonuRaporuCreate />} />

              <Route
                path="/eskep/ogrenci/"
                element={<ESKEPStudent />}
              />
              <Route
                path="/eskep/ogrenci/kursolustur"
                element={<OdevCreate />}
              />
              <Route
                path="/eskep/ogrenci/dersanket"
                element={<DersSonuAnketi />}
              />
              <Route path="/stajer/odevs/" element={<ESKEPstajerOdevs />} />
              <Route path="/stajer/kitaptahlils/" element={<ESKEPstajerOdevs />} />
              <Route path="/stajer/dersonuraporus/" element={<ESKEPstajerOdevs />} />
              <Route path="/instructor/odevs/" element={<ESKEPinstructorOdevs />} />
              <Route
                path="/instructor/odevs/:enrollment_id/"
                element={<ESKEPinstructorOdevDetail />}
              />
              {/* Agent Routes */}
              <Route path="/agent/hafizbilgi/list/" element={<AgentHafizBilgiList />} />
              <Route
                path="/hafizbilgi/create-hafizbilgi/"
                element={<HafizBilgiCreate />}
              />
              <Route
                path="/hafizbilgi/crudtable/"
                element={<CrudTableDeneme />}
              />

              {/*Admin Routes*/}
              <Route
                path="/admin/OrganizationChart/"
                element={<OrganizationChart />}
              />


              {/* Student Routes */}
              <Route
                path="/student/dashboard/"
                element={<StudentDashboard />}
              />
              <Route path="/student/courses/" element={<StudentCourses />} />
              <Route
                path="/student/courses/:enrollment_id/"
                element={<StudentCourseDetail />}
              />
              <Route path="/student/wishlist/" element={<Wishlist />} />
              <Route path="/student/profile/" element={<StudentProfile />} />
              <Route
                path="/student/change-password/"
                element={<StudentChangePassword />}
              />

              {/* Teacher Routes */}
              <Route path="/instructor/dashboard/" element={<Dashboard />} />
              <Route path="/instructor/courses/" element={<Courses />} />
              <Route path="/instructor/reviews/" element={<Review />} />
              <Route path="/instructor/students/" element={<Students />} />
              <Route path="/instructor/earning/" element={<Earning />} />
              <Route path="/instructor/orders/" element={<Orders />} />
              <Route path="/instructor/coupon/" element={<Coupon />} />
              <Route
                path="/instructor/notifications/"
                element={<TeacherNotification />}
              />
              <Route path="/instructor/question-answer/" element={<QA />} />
              <Route
                path="/instructor/change-password/"
                element={<ChangePassword />}
              />
              <Route path="/instructor/profile/" element={<Profile />} />
              <Route
                path="/instructor/create-course/"
                element={<CourseCreate />}
              />
              <Route
                path="/instructor/edit-course/:course_id/"
                element={<CourseEdit />}
              />
            
            </Routes>
          </MainWrapper>
        </BrowserRouter>
      </ProfileContext.Provider>
    </CartContext.Provider>
  );
}

export default App;
