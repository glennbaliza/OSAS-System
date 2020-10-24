-- phpMyAdmin SQL Dump
-- version 4.9.2
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Oct 24, 2020 at 08:27 PM
-- Server version: 10.4.10-MariaDB
-- PHP Version: 7.3.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `osas`
--

-- --------------------------------------------------------

--
-- Table structure for table `auth_group`
--

CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL,
  `name` varchar(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `auth_group_permissions`
--

CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `auth_permission`
--

CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `auth_permission`
--

INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
(1, 'Can add log entry', 1, 'add_logentry'),
(2, 'Can change log entry', 1, 'change_logentry'),
(3, 'Can delete log entry', 1, 'delete_logentry'),
(4, 'Can view log entry', 1, 'view_logentry'),
(5, 'Can add permission', 2, 'add_permission'),
(6, 'Can change permission', 2, 'change_permission'),
(7, 'Can delete permission', 2, 'delete_permission'),
(8, 'Can view permission', 2, 'view_permission'),
(9, 'Can add group', 3, 'add_group'),
(10, 'Can change group', 3, 'change_group'),
(11, 'Can delete group', 3, 'delete_group'),
(12, 'Can view group', 3, 'view_group'),
(13, 'Can add user', 4, 'add_user'),
(14, 'Can change user', 4, 'change_user'),
(15, 'Can delete user', 4, 'delete_user'),
(16, 'Can view user', 4, 'view_user'),
(17, 'Can add content type', 5, 'add_contenttype'),
(18, 'Can change content type', 5, 'change_contenttype'),
(19, 'Can delete content type', 5, 'delete_contenttype'),
(20, 'Can view content type', 5, 'view_contenttype'),
(21, 'Can add session', 6, 'add_session'),
(22, 'Can change session', 6, 'change_session'),
(23, 'Can delete session', 6, 'delete_session'),
(24, 'Can view session', 6, 'view_session'),
(25, 'Can add osas_r_course', 7, 'add_osas_r_course'),
(26, 'Can change osas_r_course', 7, 'change_osas_r_course'),
(27, 'Can delete osas_r_course', 7, 'delete_osas_r_course'),
(28, 'Can view osas_r_course', 7, 'view_osas_r_course'),
(29, 'Can add osas_r_section_and_year', 8, 'add_osas_r_section_and_year'),
(30, 'Can change osas_r_section_and_year', 8, 'change_osas_r_section_and_year'),
(31, 'Can delete osas_r_section_and_year', 8, 'delete_osas_r_section_and_year'),
(32, 'Can view osas_r_section_and_year', 8, 'view_osas_r_section_and_year'),
(33, 'Can add osas_r_personal_info', 9, 'add_osas_r_personal_info'),
(34, 'Can change osas_r_personal_info', 9, 'change_osas_r_personal_info'),
(35, 'Can delete osas_r_personal_info', 9, 'delete_osas_r_personal_info'),
(36, 'Can view osas_r_personal_info', 9, 'view_osas_r_personal_info'),
(37, 'Can add osas_r_stud_contact', 10, 'add_osas_r_stud_contact'),
(38, 'Can change osas_r_stud_contact', 10, 'change_osas_r_stud_contact'),
(39, 'Can delete osas_r_stud_contact', 10, 'delete_osas_r_stud_contact'),
(40, 'Can view osas_r_stud_contact', 10, 'view_osas_r_stud_contact'),
(41, 'Can add osas_r_emergency_contact', 11, 'add_osas_r_emergency_contact'),
(42, 'Can change osas_r_emergency_contact', 11, 'change_osas_r_emergency_contact'),
(43, 'Can delete osas_r_emergency_contact', 11, 'delete_osas_r_emergency_contact'),
(44, 'Can view osas_r_emergency_contact', 11, 'view_osas_r_emergency_contact'),
(45, 'Can add osas_t_id', 12, 'add_osas_t_id'),
(46, 'Can change osas_t_id', 12, 'change_osas_t_id'),
(47, 'Can delete osas_t_id', 12, 'delete_osas_t_id'),
(48, 'Can view osas_t_id', 12, 'view_osas_t_id'),
(49, 'Can add osas_t_admission', 13, 'add_osas_t_admission'),
(50, 'Can change osas_t_admission', 13, 'change_osas_t_admission'),
(51, 'Can delete osas_t_admission', 13, 'delete_osas_t_admission'),
(52, 'Can view osas_t_admission', 13, 'view_osas_t_admission');

-- --------------------------------------------------------

--
-- Table structure for table `auth_user`
--

CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `auth_user_groups`
--

CREATE TABLE `auth_user_groups` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `auth_user_user_permissions`
--

CREATE TABLE `auth_user_user_permissions` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `django_admin_log`
--

CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext DEFAULT NULL,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) UNSIGNED NOT NULL CHECK (`action_flag` >= 0),
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `django_content_type`
--

CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(1, 'admin', 'logentry'),
(3, 'auth', 'group'),
(2, 'auth', 'permission'),
(4, 'auth', 'user'),
(5, 'contenttypes', 'contenttype'),
(7, 'OsasSystem', 'osas_r_course'),
(11, 'OsasSystem', 'osas_r_emergency_contact'),
(9, 'OsasSystem', 'osas_r_personal_info'),
(8, 'OsasSystem', 'osas_r_section_and_year'),
(10, 'OsasSystem', 'osas_r_stud_contact'),
(13, 'OsasSystem', 'osas_t_admission'),
(12, 'OsasSystem', 'osas_t_id'),
(6, 'sessions', 'session');

-- --------------------------------------------------------

--
-- Table structure for table `django_migrations`
--

CREATE TABLE `django_migrations` (
  `id` int(11) NOT NULL,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'contenttypes', '0001_initial', '2020-10-24 17:55:44.163106'),
(2, 'auth', '0001_initial', '2020-10-24 17:55:46.263068'),
(3, 'admin', '0001_initial', '2020-10-24 17:55:56.063056'),
(4, 'admin', '0002_logentry_remove_auto_add', '2020-10-24 17:55:59.325087'),
(5, 'admin', '0003_logentry_add_action_flag_choices', '2020-10-24 17:55:59.371088'),
(6, 'contenttypes', '0002_remove_content_type_name', '2020-10-24 17:56:00.522056'),
(7, 'auth', '0002_alter_permission_name_max_length', '2020-10-24 17:56:02.018054'),
(8, 'auth', '0003_alter_user_email_max_length', '2020-10-24 17:56:02.249086'),
(9, 'auth', '0004_alter_user_username_opts', '2020-10-24 17:56:02.377059'),
(10, 'auth', '0005_alter_user_last_login_null', '2020-10-24 17:56:03.197094'),
(11, 'auth', '0006_require_contenttypes_0002', '2020-10-24 17:56:03.238071'),
(12, 'auth', '0007_alter_validators_add_error_messages', '2020-10-24 17:56:03.298057'),
(13, 'auth', '0008_alter_user_username_max_length', '2020-10-24 17:56:03.749076'),
(14, 'auth', '0009_alter_user_last_name_max_length', '2020-10-24 17:56:03.874054'),
(15, 'auth', '0010_alter_group_name_max_length', '2020-10-24 17:56:04.193060'),
(16, 'auth', '0011_update_proxy_permissions', '2020-10-24 17:56:04.314090'),
(17, 'sessions', '0001_initial', '2020-10-24 17:56:04.969082'),
(18, 'OsasSystem', '0001_initial', '2020-10-24 17:57:26.781372'),
(19, 'OsasSystem', '0002_osas_r_section_and_year', '2020-10-24 17:59:15.217406'),
(20, 'OsasSystem', '0003_osas_r_personal_info', '2020-10-24 17:59:52.285394'),
(21, 'OsasSystem', '0004_osas_r_stud_contact', '2020-10-24 18:00:21.248417'),
(22, 'OsasSystem', '0005_osas_r_emergency_contact', '2020-10-24 18:00:49.333369'),
(23, 'OsasSystem', '0006_osas_t_id', '2020-10-24 18:16:13.447644'),
(24, 'OsasSystem', '0007_osas_t_admission', '2020-10-24 18:20:19.487679');

-- --------------------------------------------------------

--
-- Table structure for table `django_session`
--

CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `osassystem_osas_r_course`
--

CREATE TABLE `osassystem_osas_r_course` (
  `course_id` int(11) NOT NULL,
  `course_short` varchar(50) NOT NULL,
  `course_full` varchar(250) NOT NULL,
  `status` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `osassystem_osas_r_emergency_contact`
--

CREATE TABLE `osassystem_osas_r_emergency_contact` (
  `e_contact_id` int(11) NOT NULL,
  `stud_e_name` varchar(50) NOT NULL,
  `stud_e_address` varchar(50) NOT NULL,
  `e_m_number` bigint(20) NOT NULL,
  `e_t_number` bigint(20) NOT NULL,
  `date_created` date NOT NULL,
  `date_updated` date NOT NULL,
  `stud_id_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `osassystem_osas_r_personal_info`
--

CREATE TABLE `osassystem_osas_r_personal_info` (
  `stud_id` int(11) NOT NULL,
  `stud_no` varchar(13) NOT NULL,
  `stud_lname` varchar(50) NOT NULL,
  `stud_fname` varchar(50) NOT NULL,
  `stud_mname` varchar(50) NOT NULL,
  `stud_birthdate` date NOT NULL,
  `stud_gender` varchar(10) NOT NULL,
  `stud_address` varchar(50) NOT NULL,
  `stud_email` varchar(50) NOT NULL,
  `stud_hs` varchar(50) NOT NULL,
  `stud_hs_add` varchar(50) NOT NULL,
  `date_created` date NOT NULL,
  `date_updated` date NOT NULL,
  `stud_course_id` int(11) NOT NULL,
  `stud_sec_year_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `osassystem_osas_r_section_and_year`
--

CREATE TABLE `osassystem_osas_r_section_and_year` (
  `yas_id` int(11) NOT NULL,
  `yas_descriptions` varchar(250) NOT NULL,
  `yas_dateregistered` date NOT NULL,
  `status` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `osassystem_osas_r_stud_contact`
--

CREATE TABLE `osassystem_osas_r_stud_contact` (
  `stud_contact_id` int(11) NOT NULL,
  `stud_m_number` bigint(20) NOT NULL,
  `stud_t_number` bigint(20) NOT NULL,
  `date_created` date NOT NULL,
  `date_updated` date NOT NULL,
  `stud_id_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `osassystem_osas_t_admission`
--

CREATE TABLE `osassystem_osas_t_admission` (
  `admission_id` int(11) NOT NULL,
  `request_name` varchar(50) NOT NULL,
  `request_detail` varchar(50) NOT NULL,
  `admission_status` varchar(50) NOT NULL,
  `admission_stud_id_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `osassystem_osas_t_id`
--

CREATE TABLE `osassystem_osas_t_id` (
  `request_id` int(11) NOT NULL,
  `date_created` date NOT NULL,
  `date_updated` date NOT NULL,
  `lost_id_status` int(11) NOT NULL,
  `lost_stud_id_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `auth_group`
--
ALTER TABLE `auth_group`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indexes for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  ADD KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`);

--
-- Indexes for table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`);

--
-- Indexes for table `auth_user`
--
ALTER TABLE `auth_user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Indexes for table `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  ADD KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`);

--
-- Indexes for table `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  ADD KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`);

--
-- Indexes for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD PRIMARY KEY (`id`),
  ADD KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  ADD KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`);

--
-- Indexes for table `django_content_type`
--
ALTER TABLE `django_content_type`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`);

--
-- Indexes for table `django_migrations`
--
ALTER TABLE `django_migrations`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `django_session`
--
ALTER TABLE `django_session`
  ADD PRIMARY KEY (`session_key`),
  ADD KEY `django_session_expire_date_a5c62663` (`expire_date`);

--
-- Indexes for table `osassystem_osas_r_course`
--
ALTER TABLE `osassystem_osas_r_course`
  ADD PRIMARY KEY (`course_id`);

--
-- Indexes for table `osassystem_osas_r_emergency_contact`
--
ALTER TABLE `osassystem_osas_r_emergency_contact`
  ADD PRIMARY KEY (`e_contact_id`),
  ADD KEY `OsasSystem_osas_r_em_stud_id_id_f0cb4a14_fk_OsasSyste` (`stud_id_id`);

--
-- Indexes for table `osassystem_osas_r_personal_info`
--
ALTER TABLE `osassystem_osas_r_personal_info`
  ADD PRIMARY KEY (`stud_id`),
  ADD UNIQUE KEY `stud_no` (`stud_no`),
  ADD KEY `OsasSystem_osas_r_pe_stud_course_id_036d913f_fk_OsasSyste` (`stud_course_id`),
  ADD KEY `OsasSystem_osas_r_pe_stud_sec_year_id_2a0a0331_fk_OsasSyste` (`stud_sec_year_id`);

--
-- Indexes for table `osassystem_osas_r_section_and_year`
--
ALTER TABLE `osassystem_osas_r_section_and_year`
  ADD PRIMARY KEY (`yas_id`);

--
-- Indexes for table `osassystem_osas_r_stud_contact`
--
ALTER TABLE `osassystem_osas_r_stud_contact`
  ADD PRIMARY KEY (`stud_contact_id`),
  ADD KEY `OsasSystem_osas_r_st_stud_id_id_ec5c769b_fk_OsasSyste` (`stud_id_id`);

--
-- Indexes for table `osassystem_osas_t_admission`
--
ALTER TABLE `osassystem_osas_t_admission`
  ADD PRIMARY KEY (`admission_id`),
  ADD KEY `OsasSystem_osas_t_ad_admission_stud_id_id_1f326193_fk_OsasSyste` (`admission_stud_id_id`);

--
-- Indexes for table `osassystem_osas_t_id`
--
ALTER TABLE `osassystem_osas_t_id`
  ADD PRIMARY KEY (`request_id`),
  ADD KEY `OsasSystem_osas_t_id_lost_stud_id_id_4cdb27d6_fk_OsasSyste` (`lost_stud_id_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `auth_group`
--
ALTER TABLE `auth_group`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_permission`
--
ALTER TABLE `auth_permission`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=53;

--
-- AUTO_INCREMENT for table `auth_user`
--
ALTER TABLE `auth_user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `django_content_type`
--
ALTER TABLE `django_content_type`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- AUTO_INCREMENT for table `django_migrations`
--
ALTER TABLE `django_migrations`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=25;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);

--
-- Constraints for table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);

--
-- Constraints for table `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  ADD CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  ADD CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `osassystem_osas_r_emergency_contact`
--
ALTER TABLE `osassystem_osas_r_emergency_contact`
  ADD CONSTRAINT `OsasSystem_osas_r_em_stud_id_id_f0cb4a14_fk_OsasSyste` FOREIGN KEY (`stud_id_id`) REFERENCES `osassystem_osas_r_personal_info` (`stud_id`);

--
-- Constraints for table `osassystem_osas_r_personal_info`
--
ALTER TABLE `osassystem_osas_r_personal_info`
  ADD CONSTRAINT `OsasSystem_osas_r_pe_stud_course_id_036d913f_fk_OsasSyste` FOREIGN KEY (`stud_course_id`) REFERENCES `osassystem_osas_r_course` (`course_id`),
  ADD CONSTRAINT `OsasSystem_osas_r_pe_stud_sec_year_id_2a0a0331_fk_OsasSyste` FOREIGN KEY (`stud_sec_year_id`) REFERENCES `osassystem_osas_r_section_and_year` (`yas_id`);

--
-- Constraints for table `osassystem_osas_r_stud_contact`
--
ALTER TABLE `osassystem_osas_r_stud_contact`
  ADD CONSTRAINT `OsasSystem_osas_r_st_stud_id_id_ec5c769b_fk_OsasSyste` FOREIGN KEY (`stud_id_id`) REFERENCES `osassystem_osas_r_personal_info` (`stud_id`);

--
-- Constraints for table `osassystem_osas_t_admission`
--
ALTER TABLE `osassystem_osas_t_admission`
  ADD CONSTRAINT `OsasSystem_osas_t_ad_admission_stud_id_id_1f326193_fk_OsasSyste` FOREIGN KEY (`admission_stud_id_id`) REFERENCES `osassystem_osas_r_personal_info` (`stud_id`);

--
-- Constraints for table `osassystem_osas_t_id`
--
ALTER TABLE `osassystem_osas_t_id`
  ADD CONSTRAINT `OsasSystem_osas_t_id_lost_stud_id_id_4cdb27d6_fk_OsasSyste` FOREIGN KEY (`lost_stud_id_id`) REFERENCES `osassystem_osas_r_personal_info` (`stud_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
