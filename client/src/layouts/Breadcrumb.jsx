import PropTypes from "prop-types";
import { useLocation } from 'react-router-dom';
import { Breadcrumb } from "antd"


const generateBreadcrumbs = (data, pathnames, breadcrumbs) => {
  for (let i = 0; i < data.length; i++) {
    const item = data[i];
    if (item.path === pathnames[0]) {
      pathnames.shift();
      breadcrumbs.push(item);
      if (item.children) {
        generateBreadcrumbs(item.children, pathnames, breadcrumbs);
      }
      break;
    }
  }
};


export default function MyBreadcrumb(routes) {

  const location = useLocation();
  const pathnames = location.pathname.split('/').filter((x) => x);
  var breadcrumbs = [{ path: "/", title: 'Home' }];

  generateBreadcrumbs(routes.routes, pathnames, breadcrumbs);
  console.log(breadcrumbs)

  // const rs = matchRoutes(routes.routes, location.pathname)
  // console.log(rs)

  return (
    <Breadcrumb items={breadcrumbs} />
  );

}
MyBreadcrumb.prototype = {
  routes: PropTypes.array
}