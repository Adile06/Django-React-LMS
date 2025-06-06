import React from "react";
import { Link } from "react-router-dom";

function Sidebar() {
  return (
    <div className="col-lg-2 col-md-4 col-12">
      <nav className="navbar navbar-expand-md shadow-sm mb-4 mb-lg-0 sidenav">
        <a
          className="d-xl-none d-lg-none d-md-none text-inherit fw-bold text-decoration-none text-dark p-3"
          href="#"
        >
          Menu
        </a>
        <button
          className="navbar-toggler d-md-none icon-shape icon-sm rounded bg-primary text-light m-3"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#sidenav"
          aria-controls="sidenav"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span className="bi bi-grid" />
        </button>
        <div className="collapse navbar-collapse p-3" id="sidenav">
          <div className="navbar-nav flex-column">
            <ul className="list-unstyled ms-n2 mb-4">
              <li className="nav-item">
                <Link className="nav-link" to={`/student/dashboard/`}>
                  {" "}
                  <i className="bi bi-grid-fill"></i>Panel
                </Link>
              </li>
              <li className="nav-item">
                <Link className="nav-link" to={`/eskepstajer/odevs/`}>
                  <i className="fas fa-tasks"></i> Ödevlerim
                </Link>
              </li>
              <li className="nav-item">
                <Link className="nav-link" to={`/eskepstajer/derssonuraporus/`}>
                  <i className="fas fa-file-alt"></i> Ders Sonu Raporlarım
                </Link>
              </li>
              <li className="nav-item">
                <Link className="nav-link" to={`/eskepstajer/kitaptahlileris/`}>
                  <i className="fas fa-book-reader"></i> Kitap Tahlillerim
                </Link>
              </li>
              <li className="nav-item">
                <Link className="nav-link" to={`/eskepstajer/projes/`}>
                  <i className="fas fa-lightbulb"></i> Projelerim
                </Link>
              </li>
              <li className="nav-item">
                <Link className="nav-link" to={`/student/wishlist/`}>
                  {" "}
                  <i className="fas fa-heart"></i> İstekler{" "}
                </Link>
              </li>
            </ul>

            {/* Navbar header */}
            <span className="navbar-header mb-3">Hesap Ayarları</span>
            <ul className="list-unstyled ms-n2 mb-0">
              <li className="nav-item">
                <Link className="nav-link" to={`/student/profile/`}>
                  {" "}
                  <i className="fas fa-edit"></i> Profil Düzenle
                </Link>
              </li>
              <li className="nav-item ">
                <Link className="nav-link" to={`/student/change-password/`}>
                  {" "}
                  <i className="fas fa-lock"></i> Şifre Değiştir
                </Link>
              </li>
              <li className="nav-item">
                <Link className="nav-link" to={`/login/`}>
                  {" "}
                  <i className="fas fa-sign-out-alt"></i> Çıkış Yap
                </Link>
              </li>
            </ul>
          </div>
        </div>
      </nav>
    </div>
  );
}

export default Sidebar;
