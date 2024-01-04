import { Layout, Menu, Button, Flex, theme } from "antd";
import {
  UserOutlined,
  LaptopOutlined,
  FolderViewOutlined,
  MenuUnfoldOutlined,
  MenuFoldOutlined,
} from "@ant-design/icons";

import { Link, Outlet, useLocation, matchRoutes } from "react-router-dom";
import { useEffect, useState } from "react";
import routers from "../routes";
import MyBreadcrumb from "./Breadcrumb";

const { Header, Content, Sider, Footer } = Layout;

export default function BasicLayout() {
  const location = useLocation();
  const [defaultSelectedKeys, setDefaultSelectedKeys] = useState([]);
  const [defaultOpenKeys, setDefaultOpenKeys] = useState([]);
  const [isInit, setIsInit] = useState(false);

  const [collapsed, setCollapsed] = useState(false);

  const {
    token: { colorBgContainer },
  } = theme.useToken();

  useEffect(() => {
    // 返回匹配到的路由数组对象，每一个对象都是一个路由对象
    const routes = matchRoutes(routers, location.pathname);
    const pathArr = [];
    if (routes !== null) {
      routes.forEach((item) => {
        const path = item.route.path;
        if (path) {
          pathArr.push(path);
        }
      });
    }

    setDefaultSelectedKeys(pathArr);
    setDefaultOpenKeys(pathArr);
    setIsInit(true);
  }, [location.pathname]);

  if (!isInit) {
    return null;
  }

  return (
    <>
      <Layout>
        <Sider
          width={200}
          className="site-layout-background"
          trigger={null}
          collapsible
          collapsed={collapsed}
        >
          <div className="logo" />
          <Menu
            theme="dark"
            mode="inline"
            defaultSelectedKeys={defaultSelectedKeys}
            defaultOpenKeys={defaultOpenKeys}
            items={[
              { key: "1", icon: <UserOutlined />, label: "nav 1" },
              { key: "2", icon: <LaptopOutlined />, label: "nav 2" },
              { key: "demo", icon: <UserOutlined />, label: "Demo" },
            ]}
          ></Menu>
        </Sider>
        <Layout>
          <Header style={{ padding: 0, background: colorBgContainer }}>
            <Flex gap="middle" horizontal="true">
              <Button
                type="text"
                icon={collapsed ? <MenuUnfoldOutlined /> : <MenuFoldOutlined />}
                onClick={() => setCollapsed(!collapsed)}
                style={{ fontSize: "16px", width: 64, height: 64 }}
              />
              <Menu
                theme="dark"
                mode="horizontal"
                defaultSelectedKeys={defaultSelectedKeys}
                defaultOpenKeys={defaultOpenKeys}
                items={[
                  { key: "1", icon: <UserOutlined />, label: "nav 1" },
                  { key: "2", icon: <LaptopOutlined />, label: "nav 2" },
                  {
                    key: "demo",
                    icon: <FolderViewOutlined />,
                    label: "Demo",
                    children: [
                      {
                        key: "demo_actors",
                        label: <Link to="/demo/actors">Actors</Link>,
                      },
                      {
                        key: "demo_movie",
                        label: <Link to="/demo/movie/abc-001">Movie</Link>,
                      },
                      {
                        key: "demo_movies",
                        label: <Link to="/demo/movies">Movies</Link>,
                      },
                    ],
                  },
                ]}
              />
            </Flex>
          </Header>
          <MyBreadcrumb routes={routers} />
          <Content
            className="site-layout-background"
            style={{
              padding: 24,
              margin: 0,
              minHeight: 280,
              width: "100%",
            }}
          >
            <Outlet />
          </Content>
          <Footer>Ant Design ©2023 Created by Ant UED</Footer>
        </Layout>
      </Layout>
    </>
  );
}
