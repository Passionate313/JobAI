import React from "react";
import { Menu, Button } from "antd";
import { Link } from "react-router-dom";

import CustomScrollbars from "util/CustomScrollbars";
import SidebarLogo from "./SidebarLogo";
import {
  NAV_STYLE_NO_HEADER_EXPANDED_SIDEBAR,
  NAV_STYLE_NO_HEADER_MINI_SIDEBAR,
  THEME_TYPE_LITE,
} from "../../constants/ThemeSetting";
import {
  CREATE_RESUME,
  DASHBOARD,
  AUTO_APPLY,
  MAIL_BOX,
  SCHEDULE,
  RESUME_BUILDER,
  RESUMES,
} from "../../constants/Labels";
import { useSelector } from "react-redux";

const SidebarContent = ({ sidebarCollapsed, setSidebarCollapsed }) => {
  const { navStyle, themeType } = useSelector(({ settings }) => settings);
  const pathname = useSelector(({ common }) => common.pathname);

  const getNoHeaderClass = (navStyle) => {
    if (
      navStyle === NAV_STYLE_NO_HEADER_MINI_SIDEBAR ||
      navStyle === NAV_STYLE_NO_HEADER_EXPANDED_SIDEBAR
    ) {
      return "gx-no-header-notifications";
    }
    return "";
  };

  const selectedKeys = pathname.substr(1);
  const defaultOpenKeys = selectedKeys.split("/")[1];

  return (
    <>
      <SidebarLogo
        sidebarCollapsed={sidebarCollapsed}
        setSidebarCollapsed={setSidebarCollapsed}
      />
      <div className="gx-sidebar-content">
        <div
          className={`gx-sidebar-notifications ${getNoHeaderClass(navStyle)}`}
        >
          <Button type="primary">{CREATE_RESUME}</Button>
        </div>
        <CustomScrollbars className="gx-layout-sider-scrollbar">
          <Menu
            defaultOpenKeys={[defaultOpenKeys]}
            selectedKeys={[selectedKeys]}
            theme={themeType === THEME_TYPE_LITE ? "lite" : "dark"}
            mode="inline"
          >
            <Menu.Item key="dashboard">
              <Link to="/sample">
                <i className="icon icon-data-display" />
                <span>{DASHBOARD}</span>
              </Link>
            </Menu.Item>
            <Menu.Item key="apply">
              <Link to="/sample">
                <i className="icon icon-wysiwyg" />
                <span>{AUTO_APPLY}</span>
              </Link>
            </Menu.Item>
            <Menu.Item key="mail">
              <Link to="/sample">
                <i className="icon icon-email" />
                <span>{MAIL_BOX}</span>
              </Link>
            </Menu.Item>
            <Menu.Item key="schedule">
              <Link to="/sample">
                <i className="icon icon-calendar" />
                <span>{SCHEDULE}</span>
              </Link>
            </Menu.Item>
            <Menu.SubMenu
              title={RESUMES}
              icon={<i className="icon icon-feedback" />}
            >
              <Menu.Item key="resumes">
                <Link to="/sample">
                  <span>{RESUME_BUILDER}</span>
                </Link>
              </Menu.Item>
            </Menu.SubMenu>
          </Menu>
        </CustomScrollbars>
      </div>
    </>
  );
};

export default React.memo(SidebarContent);
