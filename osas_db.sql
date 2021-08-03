-- phpMyAdmin SQL Dump
-- version 4.9.2
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Aug 03, 2021 at 06:31 AM
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
(25, 'Can add organization', 7, 'add_organization'),
(26, 'Can change organization', 7, 'change_organization'),
(27, 'Can delete organization', 7, 'delete_organization'),
(28, 'Can view organization', 7, 'view_organization'),
(29, 'Can add osas_r_auth_user', 8, 'add_osas_r_auth_user'),
(30, 'Can change osas_r_auth_user', 8, 'change_osas_r_auth_user'),
(31, 'Can delete osas_r_auth_user', 8, 'delete_osas_r_auth_user'),
(32, 'Can view osas_r_auth_user', 8, 'view_osas_r_auth_user'),
(33, 'Can add osas_r_code_title', 9, 'add_osas_r_code_title'),
(34, 'Can change osas_r_code_title', 9, 'change_osas_r_code_title'),
(35, 'Can delete osas_r_code_title', 9, 'delete_osas_r_code_title'),
(36, 'Can view osas_r_code_title', 9, 'view_osas_r_code_title'),
(37, 'Can add osas_r_course', 10, 'add_osas_r_course'),
(38, 'Can change osas_r_course', 10, 'change_osas_r_course'),
(39, 'Can delete osas_r_course', 10, 'delete_osas_r_course'),
(40, 'Can view osas_r_course', 10, 'view_osas_r_course'),
(41, 'Can add osas_r_designation_office', 11, 'add_osas_r_designation_office'),
(42, 'Can change osas_r_designation_office', 11, 'change_osas_r_designation_office'),
(43, 'Can delete osas_r_designation_office', 11, 'delete_osas_r_designation_office'),
(44, 'Can view osas_r_designation_office', 11, 'view_osas_r_designation_office'),
(45, 'Can add osas_r_disciplinary_sanction', 12, 'add_osas_r_disciplinary_sanction'),
(46, 'Can change osas_r_disciplinary_sanction', 12, 'change_osas_r_disciplinary_sanction'),
(47, 'Can delete osas_r_disciplinary_sanction', 12, 'delete_osas_r_disciplinary_sanction'),
(48, 'Can view osas_r_disciplinary_sanction', 12, 'view_osas_r_disciplinary_sanction'),
(49, 'Can add osas_r_personal_info', 13, 'add_osas_r_personal_info'),
(50, 'Can change osas_r_personal_info', 13, 'change_osas_r_personal_info'),
(51, 'Can delete osas_r_personal_info', 13, 'delete_osas_r_personal_info'),
(52, 'Can view osas_r_personal_info', 13, 'view_osas_r_personal_info'),
(53, 'Can add osas_r_section_and_year', 14, 'add_osas_r_section_and_year'),
(54, 'Can change osas_r_section_and_year', 14, 'change_osas_r_section_and_year'),
(55, 'Can delete osas_r_section_and_year', 14, 'delete_osas_r_section_and_year'),
(56, 'Can view osas_r_section_and_year', 14, 'view_osas_r_section_and_year'),
(57, 'Can add osas_r_userrole', 15, 'add_osas_r_userrole'),
(58, 'Can change osas_r_userrole', 15, 'change_osas_r_userrole'),
(59, 'Can delete osas_r_userrole', 15, 'delete_osas_r_userrole'),
(60, 'Can view osas_r_userrole', 15, 'view_osas_r_userrole'),
(61, 'Can add osas_t_excuse', 16, 'add_osas_t_excuse'),
(62, 'Can change osas_t_excuse', 16, 'change_osas_t_excuse'),
(63, 'Can delete osas_t_excuse', 16, 'delete_osas_t_excuse'),
(64, 'Can view osas_t_excuse', 16, 'view_osas_t_excuse'),
(65, 'Can add osas_t_id', 17, 'add_osas_t_id'),
(66, 'Can change osas_t_id', 17, 'change_osas_t_id'),
(67, 'Can delete osas_t_id', 17, 'delete_osas_t_id'),
(68, 'Can view osas_t_id', 17, 'view_osas_t_id'),
(69, 'Can add osas_t_sanction', 18, 'add_osas_t_sanction'),
(70, 'Can change osas_t_sanction', 18, 'change_osas_t_sanction'),
(71, 'Can delete osas_t_sanction', 18, 'delete_osas_t_sanction'),
(72, 'Can view osas_t_sanction', 18, 'view_osas_t_sanction'),
(73, 'Can add osas_t_complaint', 19, 'add_osas_t_complaint'),
(74, 'Can change osas_t_complaint', 19, 'change_osas_t_complaint'),
(75, 'Can delete osas_t_complaint', 19, 'delete_osas_t_complaint'),
(76, 'Can view osas_t_complaint', 19, 'view_osas_t_complaint'),
(77, 'Can add osas_notif', 20, 'add_osas_notif'),
(78, 'Can change osas_notif', 20, 'change_osas_notif'),
(79, 'Can delete osas_notif', 20, 'delete_osas_notif'),
(80, 'Can view osas_notif', 20, 'view_osas_notif'),
(81, 'Can add organization_chat', 21, 'add_organization_chat'),
(82, 'Can change organization_chat', 21, 'change_organization_chat'),
(83, 'Can delete organization_chat', 21, 'delete_organization_chat'),
(84, 'Can view organization_chat', 21, 'view_organization_chat'),
(85, 'Can add org_concept_paper', 22, 'add_org_concept_paper'),
(86, 'Can change org_concept_paper', 22, 'change_org_concept_paper'),
(87, 'Can delete org_concept_paper', 22, 'delete_org_concept_paper'),
(88, 'Can view org_concept_paper', 22, 'view_org_concept_paper'),
(89, 'Can add org_accreditation', 23, 'add_org_accreditation'),
(90, 'Can change org_accreditation', 23, 'change_org_accreditation'),
(91, 'Can delete org_accreditation', 23, 'delete_org_accreditation'),
(92, 'Can view org_accreditation', 23, 'view_org_accreditation'),
(93, 'Can add classroom', 24, 'add_classroom'),
(94, 'Can change classroom', 24, 'change_classroom'),
(95, 'Can delete classroom', 24, 'delete_classroom'),
(96, 'Can view classroom', 24, 'view_classroom'),
(97, 'Can add concept_paper_title', 25, 'add_concept_paper_title'),
(98, 'Can change concept_paper_title', 25, 'change_concept_paper_title'),
(99, 'Can delete concept_paper_title', 25, 'delete_concept_paper_title'),
(100, 'Can view concept_paper_title', 25, 'view_concept_paper_title'),
(101, 'Can add fund', 26, 'add_fund'),
(102, 'Can change fund', 26, 'change_fund'),
(103, 'Can delete fund', 26, 'delete_fund'),
(104, 'Can view fund', 26, 'view_fund'),
(105, 'Can add officer', 27, 'add_officer'),
(106, 'Can change officer', 27, 'change_officer'),
(107, 'Can delete officer', 27, 'delete_officer'),
(108, 'Can view officer', 27, 'view_officer'),
(109, 'Can add fund_file', 28, 'add_fund_file'),
(110, 'Can change fund_file', 28, 'change_fund_file'),
(111, 'Can delete fund_file', 28, 'delete_fund_file'),
(112, 'Can view fund_file', 28, 'view_fund_file'),
(113, 'Can add osas_t_id_file', 29, 'add_osas_t_id_file'),
(114, 'Can change osas_t_id_file', 29, 'change_osas_t_id_file'),
(115, 'Can delete osas_t_id_file', 29, 'delete_osas_t_id_file'),
(116, 'Can view osas_t_id_file', 29, 'view_osas_t_id_file');

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
(24, 'OsasSystem', 'classroom'),
(25, 'OsasSystem', 'concept_paper_title'),
(26, 'OsasSystem', 'fund'),
(28, 'OsasSystem', 'fund_file'),
(27, 'OsasSystem', 'officer'),
(7, 'OsasSystem', 'organization'),
(21, 'OsasSystem', 'organization_chat'),
(23, 'OsasSystem', 'org_accreditation'),
(22, 'OsasSystem', 'org_concept_paper'),
(20, 'OsasSystem', 'osas_notif'),
(8, 'OsasSystem', 'osas_r_auth_user'),
(9, 'OsasSystem', 'osas_r_code_title'),
(10, 'OsasSystem', 'osas_r_course'),
(11, 'OsasSystem', 'osas_r_designation_office'),
(12, 'OsasSystem', 'osas_r_disciplinary_sanction'),
(13, 'OsasSystem', 'osas_r_personal_info'),
(14, 'OsasSystem', 'osas_r_section_and_year'),
(15, 'OsasSystem', 'osas_r_userrole'),
(19, 'OsasSystem', 'osas_t_complaint'),
(16, 'OsasSystem', 'osas_t_excuse'),
(17, 'OsasSystem', 'osas_t_id'),
(29, 'OsasSystem', 'osas_t_id_file'),
(18, 'OsasSystem', 'osas_t_sanction'),
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
(1, 'OsasSystem', '0001_initial', '2021-05-06 05:48:26.609131'),
(2, 'contenttypes', '0001_initial', '2021-05-06 05:48:56.103222'),
(3, 'auth', '0001_initial', '2021-05-06 05:49:00.111224'),
(4, 'admin', '0001_initial', '2021-05-06 05:49:11.455226'),
(5, 'admin', '0002_logentry_remove_auto_add', '2021-05-06 05:49:14.111230'),
(6, 'admin', '0003_logentry_add_action_flag_choices', '2021-05-06 05:49:14.199220'),
(7, 'contenttypes', '0002_remove_content_type_name', '2021-05-06 05:49:15.279220'),
(8, 'auth', '0002_alter_permission_name_max_length', '2021-05-06 05:49:16.735223'),
(9, 'auth', '0003_alter_user_email_max_length', '2021-05-06 05:49:16.871230'),
(10, 'auth', '0004_alter_user_username_opts', '2021-05-06 05:49:16.943227'),
(11, 'auth', '0005_alter_user_last_login_null', '2021-05-06 05:49:17.823225'),
(12, 'auth', '0006_require_contenttypes_0002', '2021-05-06 05:49:17.879224'),
(13, 'auth', '0007_alter_validators_add_error_messages', '2021-05-06 05:49:17.991239'),
(14, 'auth', '0008_alter_user_username_max_length', '2021-05-06 05:49:18.383220'),
(15, 'auth', '0009_alter_user_last_name_max_length', '2021-05-06 05:49:18.639223'),
(16, 'auth', '0010_alter_group_name_max_length', '2021-05-06 05:49:18.903223'),
(17, 'auth', '0011_update_proxy_permissions', '2021-05-06 05:49:19.079228'),
(18, 'sessions', '0001_initial', '2021-05-06 05:49:19.655223'),
(19, 'OsasSystem', '0002_auto_20210510_0755', '2021-05-09 23:56:00.401038'),
(20, 'OsasSystem', '0003_auto_20210510_0759', '2021-05-09 23:59:12.906170'),
(21, 'OsasSystem', '0004_auto_20210511_0755', '2021-05-10 23:56:03.094975'),
(22, 'OsasSystem', '0005_auto_20210512_1311', '2021-05-12 05:12:02.641596'),
(23, 'OsasSystem', '0006_auto_20210514_1039', '2021-05-14 02:39:31.718968'),
(24, 'OsasSystem', '0007_auto_20210514_1056', '2021-05-14 02:56:27.757609'),
(25, 'OsasSystem', '0008_auto_20210514_1141', '2021-05-14 03:41:22.681532'),
(26, 'OsasSystem', '0009_auto_20210514_1312', '2021-05-14 05:12:32.980088'),
(27, 'OsasSystem', '0010_auto_20210514_1316', '2021-05-14 05:16:46.677397'),
(28, 'OsasSystem', '0011_auto_20210514_1317', '2021-05-14 05:17:08.385565'),
(29, 'OsasSystem', '0012_auto_20210514_1320', '2021-05-14 05:20:21.074754'),
(30, 'OsasSystem', '0013_auto_20210514_1321', '2021-05-14 05:21:53.638192'),
(31, 'OsasSystem', '0014_auto_20210517_0731', '2021-05-16 23:31:24.754190'),
(32, 'OsasSystem', '0015_auto_20210517_0739', '2021-05-16 23:39:15.128155'),
(33, 'OsasSystem', '0016_auto_20210519_1216', '2021-05-19 04:16:09.776672'),
(34, 'OsasSystem', '0017_auto_20210528_1027', '2021-05-28 02:27:39.817950'),
(35, 'OsasSystem', '0018_auto_20210601_1002', '2021-06-01 02:02:46.341595'),
(36, 'OsasSystem', '0019_auto_20210601_1035', '2021-06-01 02:35:58.246216'),
(37, 'OsasSystem', '0020_auto_20210602_0945', '2021-06-02 01:45:33.987854'),
(38, 'OsasSystem', '0021_auto_20210602_1157', '2021-06-02 03:58:05.271123'),
(39, 'OsasSystem', '0022_auto_20210602_1218', '2021-06-02 04:18:42.543452'),
(40, 'OsasSystem', '0023_auto_20210609_1009', '2021-06-09 02:09:48.051575'),
(41, 'OsasSystem', '0024_auto_20210614_1247', '2021-06-14 04:47:45.028773'),
(42, 'OsasSystem', '0025_auto_20210614_1409', '2021-06-14 06:09:29.613283'),
(43, 'OsasSystem', '0026_auto_20210618_0921', '2021-06-18 01:21:45.995475'),
(44, 'OsasSystem', '0027_auto_20210610_1500', '2021-06-10 07:00:09.585909'),
(45, 'OsasSystem', '0028_auto_20210618_1128', '2021-06-18 03:28:11.288431'),
(46, 'OsasSystem', '0029_auto_20210618_1304', '2021-06-18 05:04:52.336349'),
(47, 'OsasSystem', '0030_auto_20210618_1353', '2021-06-18 05:53:43.430393'),
(48, 'OsasSystem', '0031_auto_20210621_0813', '2021-06-21 00:14:17.666101'),
(49, 'OsasSystem', '0032_auto_20210622_1322', '2021-06-22 05:23:03.140606'),
(50, 'OsasSystem', '0033_auto_20210622_1327', '2021-06-22 05:27:23.895089'),
(51, 'OsasSystem', '0034_auto_20210628_1131', '2021-06-28 03:31:31.672086'),
(52, 'OsasSystem', '0035_auto_20210628_1220', '2021-06-28 04:20:15.818611'),
(53, 'OsasSystem', '0036_auto_20210628_1229', '2021-06-28 04:29:15.550990'),
(54, 'OsasSystem', '0037_auto_20210628_1229', '2021-06-28 04:29:58.495926'),
(55, 'OsasSystem', '0038_auto_20210628_1231', '2021-06-28 04:31:56.076216'),
(56, 'OsasSystem', '0039_auto_20210629_1649', '2021-06-29 08:49:12.201453'),
(57, 'OsasSystem', '0040_auto_20210629_1701', '2021-06-29 09:01:31.793975'),
(58, 'OsasSystem', '0041_auto_20210629_1709', '2021-06-29 09:09:43.230932'),
(59, 'OsasSystem', '0042_auto_20210629_1834', '2021-06-29 10:34:48.026711'),
(60, 'OsasSystem', '0043_auto_20210705_0839', '2021-07-05 00:40:06.160947'),
(61, 'OsasSystem', '0044_auto_20210705_1447', '2021-07-05 06:47:29.036699'),
(62, 'OsasSystem', '0045_auto_20210711_1045', '2021-07-11 02:46:06.679816'),
(63, 'OsasSystem', '0046_auto_20210711_1148', '2021-07-11 03:49:01.853738'),
(64, 'OsasSystem', '0047_auto_20210711_1150', '2021-07-11 03:50:57.927763'),
(65, 'OsasSystem', '0048_auto_20210711_1150', '2021-07-11 03:50:59.087727'),
(66, 'OsasSystem', '0049_auto_20210720_1236', '2021-07-20 04:36:46.099938'),
(67, 'OsasSystem', '0050_auto_20210720_1424', '2021-07-20 06:24:49.319359'),
(68, 'OsasSystem', '0051_auto_20210720_1425', '2021-07-20 06:25:24.254441'),
(69, 'OsasSystem', '0052_auto_20210720_1426', '2021-07-20 06:26:23.539908'),
(70, 'OsasSystem', '0053_auto_20210720_1428', '2021-07-20 06:28:10.858858'),
(71, 'OsasSystem', '0054_auto_20210724_2156', '2021-07-24 13:57:01.160929'),
(72, 'OsasSystem', '0055_auto_20210726_1340', '2021-07-26 05:40:14.066480'),
(73, 'OsasSystem', '0056_auto_20210726_1449', '2021-07-26 06:49:14.319811'),
(74, 'OsasSystem', '0057_auto_20210727_0923', '2021-07-27 01:23:31.309005'),
(75, 'OsasSystem', '0058_auto_20210729_1107', '2021-07-29 03:07:38.366999'),
(76, 'OsasSystem', '0059_auto_20210801_1241', '2021-08-01 04:41:36.198402'),
(77, 'OsasSystem', '0060_auto_20210803_1214', '2021-08-03 04:14:33.636018');

-- --------------------------------------------------------

--
-- Table structure for table `django_session`
--

CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `django_session`
--

INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
('07c25phrnj3alvb4sfmwjxmy4nn7jsxd', 'NWEwMjE2MjcyYTU2MWIxN2MyOWJlMjE4NDk0ODY2N2IxNmYwNTg3Yzp7InNlc3Npb25fdXNlcl9pZCI6MSwic2Vzc2lvbl91c2VyX2xuYW1lIjoiMSAtIDEiLCJzZXNzaW9uX2NsYXNzX3llYXIiOiIxIiwic2Vzc2lvbl9jbGFzc19zZWN0aW9uIjoiMSIsInNlc3Npb25fdXNlcl91c2VybmFtZSI6InNhbXBsZTJAZ21haWwuY29tIiwic2Vzc2lvbl91c2VyX25vIjoiZ2xlbm5AZ21haWwuY29tIiwic2Vzc2lvbl91c2VyX3JvbGUiOiJTYW1wbGUgT3JnYW5pemF0aW9uIE5hbWUiLCJzZXNzaW9uX29yZ19hYmJyIjoiU0FNUE9SRyJ9', '2021-05-28 03:04:41.824947'),
('0r7nkyimko5b24f9zfm7nwrujerat5n1', 'OWVhNDc2OGNkNDk3MzgwNWIzZTY0M2QzNjI4YWI0MWNiMTcxNzE5Mzp7InNlc3Npb25fdXNlcl9pZCI6MSwic2Vzc2lvbl91c2VyX25vIjoiMjAxNy0wMDEwMC1DTS0wIiwic2Vzc2lvbl9vcmdfYWJiciI6IlNBTVBPUkciLCJzZXNzaW9uX29yZ19zdGF0dXMiOiJBQ0NSRURJVEVEIiwic2Vzc2lvbl91c2VyX2xuYW1lIjoiYmFsaXphIiwic2Vzc2lvbl9jbGFzc195ZWFyIjoiMyAtIDEiLCJzZXNzaW9uX3VzZXJfdXNlcm5hbWUiOiJzYW50b3NAZ21haWwuY29tIiwic2Vzc2lvbl91c2VyX3JvbGUiOiJTVFVERU5UIiwic2Vzc2lvbl91c2VyX2ZuYW1lIjoiZ2xlbm4iLCJzZXNzaW9uX3VzZXJfcGFzcyI6IjEyMyJ9', '2021-08-10 04:00:22.922771'),
('2hggxj6ud2ygkw1pdk0b8m1a7uivk242', 'ZTUyYmJiMTFhYzE4MmM3YjBmMmM4MmViYTM0Y2Q1ZDhhNTJkZjIzYTp7InNlc3Npb25fdXNlcl9pZCI6MTMsInNlc3Npb25fdXNlcl9ubyI6ImFzaWxhbmpybWFya2tlbm5lZHlAZ21haWwuY29tIiwic2Vzc2lvbl9vcmdfYWJiciI6IkNPTU1JVFMiLCJzZXNzaW9uX3VzZXJfbG5hbWUiOiJBU0lMQU4iLCJzZXNzaW9uX2NsYXNzX3llYXIiOiI0IC0gMSIsInNlc3Npb25fY2xhc3Nfc2VjdGlvbiI6bnVsbCwic2Vzc2lvbl91c2VyX3VzZXJuYW1lIjoib3NhcyIsInNlc3Npb25fdXNlcl9mbmFtZSI6Ik1BUksgS0VOTkVEWSIsInNlc3Npb25fdXNlcl9wYXNzIjoiMTIzIiwic2Vzc2lvbl9vcmdfc3RhdHVzIjoiQUNDUkVESVRFRCIsInNlc3Npb25fdXNlcl9yb2xlIjoiQ29tbW9ud2VhbHRoIEluZm9ybWF0aW9uIFRlY2hub2xvZ3kgU29jaWV0eSJ9', '2021-08-17 04:14:55.318555'),
('303v4808ov34nb6keac3d5kbjarqv6q9', 'NGU1OGVlZjM2MjYzNTY4NzA5YThhM2Q3ODdlYzM2ODQwMTU3Mjc0NDp7InNlc3Npb25fdXNlcl9pZCI6MSwic2Vzc2lvbl91c2VyX2xuYW1lIjoiYmFsaXphIiwic2Vzc2lvbl91c2VyX2ZuYW1lIjoiZ2xlbm4iLCJzZXNzaW9uX3VzZXJfdXNlcm5hbWUiOiJvc2FzIiwic2Vzc2lvbl91c2VyX3Bhc3MiOiIxMjMiLCJzZXNzaW9uX3VzZXJfcm9sZSI6IkhFQUQgT1NBUyJ9', '2021-08-12 01:44:41.940587'),
('3m8q1pqi0pdpm3f9rciodpodadpue8kb', 'NGU1OGVlZjM2MjYzNTY4NzA5YThhM2Q3ODdlYzM2ODQwMTU3Mjc0NDp7InNlc3Npb25fdXNlcl9pZCI6MSwic2Vzc2lvbl91c2VyX2xuYW1lIjoiYmFsaXphIiwic2Vzc2lvbl91c2VyX2ZuYW1lIjoiZ2xlbm4iLCJzZXNzaW9uX3VzZXJfdXNlcm5hbWUiOiJvc2FzIiwic2Vzc2lvbl91c2VyX3Bhc3MiOiIxMjMiLCJzZXNzaW9uX3VzZXJfcm9sZSI6IkhFQUQgT1NBUyJ9', '2021-06-16 00:30:53.467701'),
('4o1rof9awkh9va8sde5faolvdhgo1gxl', 'NGU1OGVlZjM2MjYzNTY4NzA5YThhM2Q3ODdlYzM2ODQwMTU3Mjc0NDp7InNlc3Npb25fdXNlcl9pZCI6MSwic2Vzc2lvbl91c2VyX2xuYW1lIjoiYmFsaXphIiwic2Vzc2lvbl91c2VyX2ZuYW1lIjoiZ2xlbm4iLCJzZXNzaW9uX3VzZXJfdXNlcm5hbWUiOiJvc2FzIiwic2Vzc2lvbl91c2VyX3Bhc3MiOiIxMjMiLCJzZXNzaW9uX3VzZXJfcm9sZSI6IkhFQUQgT1NBUyJ9', '2021-06-29 11:46:03.647003'),
('4r58byteijevpsd3rqic4bbu9xz7gakh', 'NmE0YTc3MDlmNTJhOWQ2OTRmZGZkZDAxODdiZGRmOTNiNzY0MmI5ZTp7InNlc3Npb25fdXNlcl9pZCI6MSwic2Vzc2lvbl91c2VyX2xuYW1lIjoiYmFsaXphIiwic2Vzc2lvbl91c2VyX2ZuYW1lIjoiZ2xlbm4iLCJzZXNzaW9uX3VzZXJfdXNlcm5hbWUiOiJvc2FzIiwic2Vzc2lvbl91c2VyX3Bhc3MiOiIxMjMiLCJzZXNzaW9uX2NsYXNzX3llYXIiOiIxIiwic2Vzc2lvbl9jbGFzc19zZWN0aW9uIjoiMSIsInNlc3Npb25fdXNlcl9ubyI6ImdsZW5uQGdtYWlsLmNvbSIsInNlc3Npb25fb3JnX2FiYnIiOiJTQU1QT1JHIiwic2Vzc2lvbl91c2VyX3JvbGUiOiJIRUFEIE9TQVMifQ==', '2021-05-25 06:21:30.440119'),
('71es1x21ywd8kyui8j3s2ynff4cyhy91', 'NWQ2ZjcwNjk2MjU5YWY5MzBmODAwNWY0ZWM3OTc2NzM0N2JhMjJmZDp7InNlc3Npb25fdXNlcl9pZCI6MSwic2Vzc2lvbl91c2VyX2xuYW1lIjoiQkJUTEVESEUgMSAtIDEiLCJzZXNzaW9uX2NsYXNzX3llYXIiOiIxIiwic2Vzc2lvbl9jbGFzc19zZWN0aW9uIjoiMSIsInNlc3Npb25fdXNlcl91c2VybmFtZSI6InNhbXBsZTJAZ21haWwuY29tIn0=', '2021-06-07 07:10:34.667046'),
('7pyx08btzaiiewwwb39wk0kiz04aa5yv', 'NGU1OGVlZjM2MjYzNTY4NzA5YThhM2Q3ODdlYzM2ODQwMTU3Mjc0NDp7InNlc3Npb25fdXNlcl9pZCI6MSwic2Vzc2lvbl91c2VyX2xuYW1lIjoiYmFsaXphIiwic2Vzc2lvbl91c2VyX2ZuYW1lIjoiZ2xlbm4iLCJzZXNzaW9uX3VzZXJfdXNlcm5hbWUiOiJvc2FzIiwic2Vzc2lvbl91c2VyX3Bhc3MiOiIxMjMiLCJzZXNzaW9uX3VzZXJfcm9sZSI6IkhFQUQgT1NBUyJ9', '2021-07-12 04:43:54.230204'),
('8s8olan5v6e8msu04cnieqseu7kowqgg', 'NGU1OGVlZjM2MjYzNTY4NzA5YThhM2Q3ODdlYzM2ODQwMTU3Mjc0NDp7InNlc3Npb25fdXNlcl9pZCI6MSwic2Vzc2lvbl91c2VyX2xuYW1lIjoiYmFsaXphIiwic2Vzc2lvbl91c2VyX2ZuYW1lIjoiZ2xlbm4iLCJzZXNzaW9uX3VzZXJfdXNlcm5hbWUiOiJvc2FzIiwic2Vzc2lvbl91c2VyX3Bhc3MiOiIxMjMiLCJzZXNzaW9uX3VzZXJfcm9sZSI6IkhFQUQgT1NBUyJ9', '2021-06-23 02:10:08.313244'),
('90lly7xqui93lwe5kk096kdeo99pwe6t', 'ZTc0MGFkMDRmMzgzYTBmMWE5MjhkMWI2NGQ3NDg1NjNkM2MwMTM0NDp7InNlc3Npb25fdXNlcl9pZCI6MSwic2Vzc2lvbl91c2VyX2xuYW1lIjoiYmFsaXphIiwic2Vzc2lvbl9jbGFzc195ZWFyIjoiMyAtIDEiLCJzZXNzaW9uX3VzZXJfdXNlcm5hbWUiOiJvc2FzIiwic2Vzc2lvbl91c2VyX25vIjoiMjAxNy0wMDEwMC1DTS0wIiwic2Vzc2lvbl9vcmdfYWJiciI6IlNBTVBPUkciLCJzZXNzaW9uX3VzZXJfZm5hbWUiOiJnbGVubiIsInNlc3Npb25fdXNlcl9wYXNzIjoiMTIzIiwic2Vzc2lvbl91c2VyX3JvbGUiOiJIRUFEIE9TQVMifQ==', '2021-07-14 00:03:23.138904'),
('9nuldhhq7kzejjck1nfg1pqohbvyqyaj', 'NGU1OGVlZjM2MjYzNTY4NzA5YThhM2Q3ODdlYzM2ODQwMTU3Mjc0NDp7InNlc3Npb25fdXNlcl9pZCI6MSwic2Vzc2lvbl91c2VyX2xuYW1lIjoiYmFsaXphIiwic2Vzc2lvbl91c2VyX2ZuYW1lIjoiZ2xlbm4iLCJzZXNzaW9uX3VzZXJfdXNlcm5hbWUiOiJvc2FzIiwic2Vzc2lvbl91c2VyX3Bhc3MiOiIxMjMiLCJzZXNzaW9uX3VzZXJfcm9sZSI6IkhFQUQgT1NBUyJ9', '2021-06-22 03:16:29.304554'),
('b4oz7be5e6s09zj4022mtshv6hcgi33i', 'NGU1OGVlZjM2MjYzNTY4NzA5YThhM2Q3ODdlYzM2ODQwMTU3Mjc0NDp7InNlc3Npb25fdXNlcl9pZCI6MSwic2Vzc2lvbl91c2VyX2xuYW1lIjoiYmFsaXphIiwic2Vzc2lvbl91c2VyX2ZuYW1lIjoiZ2xlbm4iLCJzZXNzaW9uX3VzZXJfdXNlcm5hbWUiOiJvc2FzIiwic2Vzc2lvbl91c2VyX3Bhc3MiOiIxMjMiLCJzZXNzaW9uX3VzZXJfcm9sZSI6IkhFQUQgT1NBUyJ9', '2021-06-29 01:18:55.791391'),
('exqx3tm1cqse3lnko0o6kd04oyo9f71a', 'OWQ0NDkwMWNhOTJiNTA0OTVkYzYxOTFkYmQzNmMyYjRmYjRlZTJiMjp7InNlc3Npb25fdXNlcl9pZCI6MSwic2Vzc2lvbl91c2VyX2xuYW1lIjoiYmFsaXphIiwic2Vzc2lvbl91c2VyX2ZuYW1lIjoiZ2xlbm4iLCJzZXNzaW9uX3VzZXJfdXNlcm5hbWUiOiJvc2FzIiwic2Vzc2lvbl91c2VyX3Bhc3MiOiIxMjMiLCJzZXNzaW9uX3VzZXJfbm8iOiIyMDE3LTAwMTAwLUNNLTEiLCJzZXNzaW9uX3VzZXJfcm9sZSI6IkhFQUQgT1NBUyJ9', '2021-07-13 14:06:56.638275'),
('f3y5ztlhog8gfqk7w4k07oqllhs7btcb', 'NTFjYzczYThjNzNlYTNkM2M4ZDIzZTYwNWI2ZGEyMzI3MjIzZjE0Yzp7InNlc3Npb25fdXNlcl9pZCI6MSwic2Vzc2lvbl91c2VyX2xuYW1lIjoiQkJUTEVESEUgMSAtIDEiLCJzZXNzaW9uX2NsYXNzX3llYXIiOiIxIiwic2Vzc2lvbl9jbGFzc19zZWN0aW9uIjoiMSIsInNlc3Npb25fdXNlcl91c2VybmFtZSI6InNhbXBsZTJAZ21haWwuY29tIiwic2Vzc2lvbl91c2VyX25vIjoiZ2xlbm5AZ21haWwuY29tIiwic2Vzc2lvbl9vcmdfYWJiciI6IlNBTVBPUkciLCJzZXNzaW9uX3VzZXJfcm9sZSI6Im5vbmUifQ==', '2021-06-04 04:16:02.584179'),
('hlfvo30f6ht2yp1npw4egvw65a9jqs8k', 'MmI5YWQ1ZTcyNmY1MTEwMDk4YTUyNDUxZDQyNzMxZmNjZGYzYTNiNzp7InNlc3Npb25fdXNlcl9pZCI6MTEsInNlc3Npb25fdXNlcl9ubyI6ImdsZW5uQGdtYWlsLmNvbSIsInNlc3Npb25fb3JnX2FiYnIiOiJTQU1QT1JHIiwic2Vzc2lvbl9vcmdfc3RhdHVzIjoiSU5BQ1RJVkUiLCJzZXNzaW9uX3VzZXJfcm9sZSI6IlNhbXBsZSBPcmdhbml6YXRpb24ifQ==', '2021-08-03 06:34:21.155061'),
('ieqpqv11vzscr5k93f8d0z4tyred1c9o', 'NGU1OGVlZjM2MjYzNTY4NzA5YThhM2Q3ODdlYzM2ODQwMTU3Mjc0NDp7InNlc3Npb25fdXNlcl9pZCI6MSwic2Vzc2lvbl91c2VyX2xuYW1lIjoiYmFsaXphIiwic2Vzc2lvbl91c2VyX2ZuYW1lIjoiZ2xlbm4iLCJzZXNzaW9uX3VzZXJfdXNlcm5hbWUiOiJvc2FzIiwic2Vzc2lvbl91c2VyX3Bhc3MiOiIxMjMiLCJzZXNzaW9uX3VzZXJfcm9sZSI6IkhFQUQgT1NBUyJ9', '2021-05-21 05:43:22.689916'),
('j1bzstyuyxbaqek4jbzg0ha9dvfosccl', 'NGU1OGVlZjM2MjYzNTY4NzA5YThhM2Q3ODdlYzM2ODQwMTU3Mjc0NDp7InNlc3Npb25fdXNlcl9pZCI6MSwic2Vzc2lvbl91c2VyX2xuYW1lIjoiYmFsaXphIiwic2Vzc2lvbl91c2VyX2ZuYW1lIjoiZ2xlbm4iLCJzZXNzaW9uX3VzZXJfdXNlcm5hbWUiOiJvc2FzIiwic2Vzc2lvbl91c2VyX3Bhc3MiOiIxMjMiLCJzZXNzaW9uX3VzZXJfcm9sZSI6IkhFQUQgT1NBUyJ9', '2021-06-14 03:31:02.498402'),
('jsj8c6s1y04wi0tn5appl9mppzizlaiz', 'NGU1OGVlZjM2MjYzNTY4NzA5YThhM2Q3ODdlYzM2ODQwMTU3Mjc0NDp7InNlc3Npb25fdXNlcl9pZCI6MSwic2Vzc2lvbl91c2VyX2xuYW1lIjoiYmFsaXphIiwic2Vzc2lvbl91c2VyX2ZuYW1lIjoiZ2xlbm4iLCJzZXNzaW9uX3VzZXJfdXNlcm5hbWUiOiJvc2FzIiwic2Vzc2lvbl91c2VyX3Bhc3MiOiIxMjMiLCJzZXNzaW9uX3VzZXJfcm9sZSI6IkhFQUQgT1NBUyJ9', '2021-07-25 02:50:28.488147'),
('kx1upqj31663fsonao2g3texxujlo4jk', 'NGU1OGVlZjM2MjYzNTY4NzA5YThhM2Q3ODdlYzM2ODQwMTU3Mjc0NDp7InNlc3Npb25fdXNlcl9pZCI6MSwic2Vzc2lvbl91c2VyX2xuYW1lIjoiYmFsaXphIiwic2Vzc2lvbl91c2VyX2ZuYW1lIjoiZ2xlbm4iLCJzZXNzaW9uX3VzZXJfdXNlcm5hbWUiOiJvc2FzIiwic2Vzc2lvbl91c2VyX3Bhc3MiOiIxMjMiLCJzZXNzaW9uX3VzZXJfcm9sZSI6IkhFQUQgT1NBUyJ9', '2021-08-13 01:41:10.432776'),
('l2rcrflw19lf0eextqymsx754pqlcol0', 'NGU1OGVlZjM2MjYzNTY4NzA5YThhM2Q3ODdlYzM2ODQwMTU3Mjc0NDp7InNlc3Npb25fdXNlcl9pZCI6MSwic2Vzc2lvbl91c2VyX2xuYW1lIjoiYmFsaXphIiwic2Vzc2lvbl91c2VyX2ZuYW1lIjoiZ2xlbm4iLCJzZXNzaW9uX3VzZXJfdXNlcm5hbWUiOiJvc2FzIiwic2Vzc2lvbl91c2VyX3Bhc3MiOiIxMjMiLCJzZXNzaW9uX3VzZXJfcm9sZSI6IkhFQUQgT1NBUyJ9', '2021-07-03 12:04:12.291552'),
('l8dbosusr2kexztr8ui7hqov9bybd5kt', 'NGU1OGVlZjM2MjYzNTY4NzA5YThhM2Q3ODdlYzM2ODQwMTU3Mjc0NDp7InNlc3Npb25fdXNlcl9pZCI6MSwic2Vzc2lvbl91c2VyX2xuYW1lIjoiYmFsaXphIiwic2Vzc2lvbl91c2VyX2ZuYW1lIjoiZ2xlbm4iLCJzZXNzaW9uX3VzZXJfdXNlcm5hbWUiOiJvc2FzIiwic2Vzc2lvbl91c2VyX3Bhc3MiOiIxMjMiLCJzZXNzaW9uX3VzZXJfcm9sZSI6IkhFQUQgT1NBUyJ9', '2021-08-09 06:36:01.054968'),
('lzxr3sezvcvvhvhbnb9w4nnp8n8bgbbz', 'OWQxYjBjMWZjZDk5OTRjOWQwNjQyY2Q4ZjRlNzBlZTNkOWNlZmZmNzp7InNlc3Npb25fdXNlcl9pZCI6MTYsInNlc3Npb25fdXNlcl9ubyI6ImJhbGRvdml6b2tyaXN0aW5lam95QGdtYWlsLmNvbSIsInNlc3Npb25fb3JnX2FiYnIiOiJDSFJTIiwic2Vzc2lvbl9vcmdfc3RhdHVzIjoiQUNDUkVESVRFRCIsInNlc3Npb25fdXNlcl9yb2xlIjoiSHVtYW4gUmVzb3VyY2UgTWFuYWdlbWVudCJ9', '2021-08-13 11:16:01.314940'),
('m5lfgjc46rpda3mk0h70rmelyjar8pmz', 'NGU1OGVlZjM2MjYzNTY4NzA5YThhM2Q3ODdlYzM2ODQwMTU3Mjc0NDp7InNlc3Npb25fdXNlcl9pZCI6MSwic2Vzc2lvbl91c2VyX2xuYW1lIjoiYmFsaXphIiwic2Vzc2lvbl91c2VyX2ZuYW1lIjoiZ2xlbm4iLCJzZXNzaW9uX3VzZXJfdXNlcm5hbWUiOiJvc2FzIiwic2Vzc2lvbl91c2VyX3Bhc3MiOiIxMjMiLCJzZXNzaW9uX3VzZXJfcm9sZSI6IkhFQUQgT1NBUyJ9', '2021-08-07 12:10:32.494689'),
('mqxyc1dfu294obfgijda97ow4zf46pfj', 'NGU1OGVlZjM2MjYzNTY4NzA5YThhM2Q3ODdlYzM2ODQwMTU3Mjc0NDp7InNlc3Npb25fdXNlcl9pZCI6MSwic2Vzc2lvbl91c2VyX2xuYW1lIjoiYmFsaXphIiwic2Vzc2lvbl91c2VyX2ZuYW1lIjoiZ2xlbm4iLCJzZXNzaW9uX3VzZXJfdXNlcm5hbWUiOiJvc2FzIiwic2Vzc2lvbl91c2VyX3Bhc3MiOiIxMjMiLCJzZXNzaW9uX3VzZXJfcm9sZSI6IkhFQUQgT1NBUyJ9', '2021-06-25 01:18:37.428564'),
('mrlauyc7trov2hhqs9i0l5c43t52gfoi', 'NGU1OGVlZjM2MjYzNTY4NzA5YThhM2Q3ODdlYzM2ODQwMTU3Mjc0NDp7InNlc3Npb25fdXNlcl9pZCI6MSwic2Vzc2lvbl91c2VyX2xuYW1lIjoiYmFsaXphIiwic2Vzc2lvbl91c2VyX2ZuYW1lIjoiZ2xlbm4iLCJzZXNzaW9uX3VzZXJfdXNlcm5hbWUiOiJvc2FzIiwic2Vzc2lvbl91c2VyX3Bhc3MiOiIxMjMiLCJzZXNzaW9uX3VzZXJfcm9sZSI6IkhFQUQgT1NBUyJ9', '2021-06-02 02:05:24.178777'),
('n1coxequc4f74vp89w0765fg9jt46ajk', 'NGU1OGVlZjM2MjYzNTY4NzA5YThhM2Q3ODdlYzM2ODQwMTU3Mjc0NDp7InNlc3Npb25fdXNlcl9pZCI6MSwic2Vzc2lvbl91c2VyX2xuYW1lIjoiYmFsaXphIiwic2Vzc2lvbl91c2VyX2ZuYW1lIjoiZ2xlbm4iLCJzZXNzaW9uX3VzZXJfdXNlcm5hbWUiOiJvc2FzIiwic2Vzc2lvbl91c2VyX3Bhc3MiOiIxMjMiLCJzZXNzaW9uX3VzZXJfcm9sZSI6IkhFQUQgT1NBUyJ9', '2021-08-16 14:31:11.315365'),
('nixf61efz9mihxyu8ro225sp5d64u9ja', 'YThmZGZjM2NiZGE0NWU0MDA0YmM5MTk0ZmRkOGE2MGJhODkzNDE5MDp7InNlc3Npb25fdXNlcl9pZCI6MSwic2Vzc2lvbl91c2VyX25vIjoiZ2xlbm5AZ21haWwuY29tIiwic2Vzc2lvbl9vcmdfYWJiciI6IlNBTVBPUkciLCJzZXNzaW9uX3VzZXJfbG5hbWUiOiIxIC0gMSIsInNlc3Npb25fY2xhc3NfeWVhciI6IjEiLCJzZXNzaW9uX2NsYXNzX3NlY3Rpb24iOiIxIiwic2Vzc2lvbl91c2VyX3VzZXJuYW1lIjoic2FtcGxlMkBnbWFpbC5jb20iLCJzZXNzaW9uX3VzZXJfcm9sZSI6Im5vbmUifQ==', '2021-05-31 06:29:08.698402'),
('nt6v7w023xlvorfxmrnfh9pdei0fe8ae', 'NGU1OGVlZjM2MjYzNTY4NzA5YThhM2Q3ODdlYzM2ODQwMTU3Mjc0NDp7InNlc3Npb25fdXNlcl9pZCI6MSwic2Vzc2lvbl91c2VyX2xuYW1lIjoiYmFsaXphIiwic2Vzc2lvbl91c2VyX2ZuYW1lIjoiZ2xlbm4iLCJzZXNzaW9uX3VzZXJfdXNlcm5hbWUiOiJvc2FzIiwic2Vzc2lvbl91c2VyX3Bhc3MiOiIxMjMiLCJzZXNzaW9uX3VzZXJfcm9sZSI6IkhFQUQgT1NBUyJ9', '2021-07-06 00:48:11.201497'),
('o34hae0jh4uxqbuha13lh7iynmslk2hj', 'NTFlNzg2ODg3NTY1Mjk4ZjU1ZjZjY2ExNTI2ZmJkMTZmMTllZjFlMzp7InNlc3Npb25fdXNlcl9pZCI6MSwic2Vzc2lvbl91c2VyX2xuYW1lIjoiQkJUTEVESEUgMSAtIDEiLCJzZXNzaW9uX2NsYXNzX3llYXIiOiIxIiwic2Vzc2lvbl9jbGFzc19zZWN0aW9uIjoiMSIsInNlc3Npb25fdXNlcl91c2VybmFtZSI6InNhbXBsZTJAZ21haWwuY29tIiwic2Vzc2lvbl91c2VyX25vIjoiZ2xlbm5AZ21haWwuY29tIiwic2Vzc2lvbl91c2VyX3JvbGUiOiJTYW1wbGUgT3JnYW5pemF0aW9uIE5hbWUiLCJzZXNzaW9uX29yZ19hYmJyIjoiU0FNUE9SRyJ9', '2021-06-10 01:32:12.618122'),
('q3m8deubxbm4okdb922rfupdnv0l4a9l', 'NTk3NWVkZGNhMTQ1NDFmYTBhNzUwNzliODJmMmZiN2E4YzlmMWE2ZDp7InNlc3Npb25fdXNlcl9pZCI6MTIsInNlc3Npb25fdXNlcl9ubyI6ImFzaWxhbkBnbWFpbC5jb20iLCJzZXNzaW9uX29yZ19hYmJyIjoiU2xhcHNvaWwiLCJzZXNzaW9uX29yZ19zdGF0dXMiOiJJTkFDVElWRSIsInNlc3Npb25fdXNlcl9yb2xlIjoiSGFtYm9nIG5nIFNhZ3BybyBDcmV3In0=', '2021-08-04 15:15:14.829848'),
('q6ufnbu4xdj6agi24xhifytqi82ytttw', 'ZTdiNGM4ZmRkNmFiZTNmMmU2YTY1ZTY5MGZlNjAyYWM5YWYwOTQ0Nzp7InNlc3Npb25fdXNlcl9pZCI6MSwic2Vzc2lvbl91c2VyX2xuYW1lIjoiQkJUTEVESEUgMyAtIDEiLCJzZXNzaW9uX2NsYXNzX3llYXIiOiIzIC0gMSIsInNlc3Npb25fdXNlcl91c2VybmFtZSI6InNhbnRvc0BnbWFpbC5jb20iLCJzZXNzaW9uX3VzZXJfbm8iOiJnbGVubkBnbWFpbC5jb20iLCJzZXNzaW9uX3VzZXJfcm9sZSI6IlNhbXBsZSBPcmdhbml6YXRpb24gTmFtZSIsInNlc3Npb25fb3JnX2FiYnIiOiJTQU1QT1JHIn0=', '2021-07-12 12:31:58.664068'),
('qpajfc4zrp6ccsybs4b816818zlm3zyu', 'YmJlZWFiNTAwZDgwNjA3MzMwNzdmYTRiMzkzM2RkZjczZWJmZjNlODp7InNlc3Npb25fdXNlcl9pZCI6MSwic2Vzc2lvbl91c2VyX2xuYW1lIjoiYmFsaXphIiwic2Vzc2lvbl91c2VyX2ZuYW1lIjoiZ2xlbm4iLCJzZXNzaW9uX3VzZXJfdXNlcm5hbWUiOiJvc2FzIiwic2Vzc2lvbl91c2VyX3Bhc3MiOiIxMjMiLCJzZXNzaW9uX3VzZXJfbm8iOiJnbGVubkBnbWFpbC5jb20iLCJzZXNzaW9uX29yZ19hYmJyIjoiU0FNUE9SRyIsInNlc3Npb25fY2xhc3NfeWVhciI6IjEiLCJzZXNzaW9uX2NsYXNzX3NlY3Rpb24iOiIxIiwic2Vzc2lvbl91c2VyX3JvbGUiOiJIRUFEIE9TQVMifQ==', '2021-05-27 11:01:04.876310'),
('rp9r0upstvmwdxhfeignuqa0c6sc7chq', 'NmUzMzYwY2FjOGRjZTUwNjIyN2NmYWYyZjU0ODg5YmRkMTVhZDQyMjp7InNlc3Npb25fdXNlcl9pZCI6MSwic2Vzc2lvbl91c2VyX25vIjoiZ2xlbm5AZ21haWwuY29tIiwic2Vzc2lvbl9vcmdfYWJiciI6IlNBTVBPUkciLCJzZXNzaW9uX3VzZXJfbG5hbWUiOiJiYWxpemEiLCJzZXNzaW9uX3VzZXJfZm5hbWUiOiJnbGVubiIsInNlc3Npb25fdXNlcl91c2VybmFtZSI6Im9zYXMiLCJzZXNzaW9uX3VzZXJfcGFzcyI6IjEyMyIsInNlc3Npb25fY2xhc3NfeWVhciI6MSwic2Vzc2lvbl9jbGFzc19zZWN0aW9uIjoiMSIsInNlc3Npb25fdXNlcl9yb2xlIjoiU2FtcGxlIE9yZ2FuaXphdGlvbiBOYW1lIn0=', '2021-07-05 06:13:09.680139'),
('rtm49zrydsc9yi64cngduyo5ym41ubip', 'YWE0NjZmNGU0NzEwYmI0MTQ3NjNjZDhhYTQxNjA1MjFhNWY3ZmMwNjp7InNlc3Npb25fdXNlcl9pZCI6MSwic2Vzc2lvbl91c2VyX2xuYW1lIjoiYmFsaXphIiwic2Vzc2lvbl91c2VyX2ZuYW1lIjoiZ2xlbm4iLCJzZXNzaW9uX3VzZXJfdXNlcm5hbWUiOiJvc2FzIiwic2Vzc2lvbl91c2VyX3Bhc3MiOiIxMjMiLCJzZXNzaW9uX3VzZXJfcm9sZSI6IlNUVURFTlQiLCJzZXNzaW9uX3VzZXJfbm8iOiIyMDE3LTAwMTAwLUNNLTAifQ==', '2021-07-19 06:50:39.720802'),
('s45i9ibzsr7hvghpx6wulz5nlli1clss', 'NTFjYzczYThjNzNlYTNkM2M4ZDIzZTYwNWI2ZGEyMzI3MjIzZjE0Yzp7InNlc3Npb25fdXNlcl9pZCI6MSwic2Vzc2lvbl91c2VyX2xuYW1lIjoiQkJUTEVESEUgMSAtIDEiLCJzZXNzaW9uX2NsYXNzX3llYXIiOiIxIiwic2Vzc2lvbl9jbGFzc19zZWN0aW9uIjoiMSIsInNlc3Npb25fdXNlcl91c2VybmFtZSI6InNhbXBsZTJAZ21haWwuY29tIiwic2Vzc2lvbl91c2VyX25vIjoiZ2xlbm5AZ21haWwuY29tIiwic2Vzc2lvbl9vcmdfYWJiciI6IlNBTVBPUkciLCJzZXNzaW9uX3VzZXJfcm9sZSI6Im5vbmUifQ==', '2021-06-03 06:17:36.715877'),
('sweakse2zdqfv4ctbekp2sgz5711a5os', 'NGU1OGVlZjM2MjYzNTY4NzA5YThhM2Q3ODdlYzM2ODQwMTU3Mjc0NDp7InNlc3Npb25fdXNlcl9pZCI6MSwic2Vzc2lvbl91c2VyX2xuYW1lIjoiYmFsaXphIiwic2Vzc2lvbl91c2VyX2ZuYW1lIjoiZ2xlbm4iLCJzZXNzaW9uX3VzZXJfdXNlcm5hbWUiOiJvc2FzIiwic2Vzc2lvbl91c2VyX3Bhc3MiOiIxMjMiLCJzZXNzaW9uX3VzZXJfcm9sZSI6IkhFQUQgT1NBUyJ9', '2021-06-07 03:29:22.911898'),
('ujxflinmaeh0ft278hc9weffm7k7et8e', 'YThmZGZjM2NiZGE0NWU0MDA0YmM5MTk0ZmRkOGE2MGJhODkzNDE5MDp7InNlc3Npb25fdXNlcl9pZCI6MSwic2Vzc2lvbl91c2VyX25vIjoiZ2xlbm5AZ21haWwuY29tIiwic2Vzc2lvbl9vcmdfYWJiciI6IlNBTVBPUkciLCJzZXNzaW9uX3VzZXJfbG5hbWUiOiIxIC0gMSIsInNlc3Npb25fY2xhc3NfeWVhciI6IjEiLCJzZXNzaW9uX2NsYXNzX3NlY3Rpb24iOiIxIiwic2Vzc2lvbl91c2VyX3VzZXJuYW1lIjoic2FtcGxlMkBnbWFpbC5jb20iLCJzZXNzaW9uX3VzZXJfcm9sZSI6Im5vbmUifQ==', '2021-05-26 03:01:56.736891'),
('vwt49yigbqb3i1x5ewf11m6asgsyltnj', 'Mzk1ODQyNGI0NjQzZWZjYjZjN2RlMjA2ODc2Y2FkMmJlZmRiZWI2Njp7InNlc3Npb25fdXNlcl9pZCI6MSwic2Vzc2lvbl91c2VyX2xuYW1lIjoiQkJUTEVESEUgMSAtIDEiLCJzZXNzaW9uX3VzZXJfZm5hbWUiOiJnbGVubiIsInNlc3Npb25fdXNlcl91c2VybmFtZSI6InNhbXBsZTJAZ21haWwuY29tIiwic2Vzc2lvbl91c2VyX3Bhc3MiOiIxMjMiLCJzZXNzaW9uX3VzZXJfcm9sZSI6Im5vbmUiLCJzZXNzaW9uX2NsYXNzX3llYXIiOiIxIiwic2Vzc2lvbl9jbGFzc19zZWN0aW9uIjoiMSJ9', '2021-06-28 04:58:57.961927'),
('was0uijlzbp9u8eh3a2qo09cdek24jcs', 'MDg3NWJmY2I1N2JhMjVjMmVjOWY2NDM4MjY4NjRlZDA5ZWQ0ZjdkNTp7InNlc3Npb25fdXNlcl9pZCI6MTQsInNlc3Npb25fdXNlcl9ubyI6ImdsZW5uQGdtYWlsLmNvbSIsInNlc3Npb25fdXNlcl9sbmFtZSI6IkJBTElaQSIsInNlc3Npb25fdXNlcl9mbmFtZSI6IkdMRU5OIiwic2Vzc2lvbl91c2VyX3Bhc3MiOiIxMjMiLCJzZXNzaW9uX29yZ19hYmJyIjoiU0FNUExFIiwic2Vzc2lvbl9vcmdfc3RhdHVzIjoiQUNDUkVESVRFRCIsInNlc3Npb25fdXNlcl9yb2xlIjoibm9uZSJ9', '2021-08-14 09:01:50.795914'),
('wliimzrgm0mvji2ec9jexxznt2uz5u51', 'ODdmMjU3NTA0NzhmMTM4NmNiMTFlZTExMzgyNDA5YzFkMjRjYjM1Yzp7InNlc3Npb25fdXNlcl9pZCI6MTMsInNlc3Npb25fdXNlcl9ubyI6ImFzaWxhbmpybWFya2tlbm5lZHlAZ21haWwuY29tIiwic2Vzc2lvbl9vcmdfYWJiciI6IkNPTU1JVFMiLCJzZXNzaW9uX29yZ19zdGF0dXMiOiJBQ0NSRURJVEVEIiwic2Vzc2lvbl91c2VyX3JvbGUiOiJDb21tb253ZWFsdGggSW5mb3JtYXRpb24gVGVjaG5vbG9neSBTb2NpZXR5In0=', '2021-08-15 05:59:43.227895'),
('y6h6opjcodtaz3u8jq8dky33kkspk185', 'MTU3ZTZiNzQyNDYwZGIzZTM2YzE5Njk1MzQzOWY2NGE5NjJkNjRjZjp7InNlc3Npb25fdXNlcl9pZCI6MjgsInNlc3Npb25fdXNlcl9ubyI6ImdsZW5uQGdtYWlsLmNvbSIsInNlc3Npb25fb3JnX2FiYnIiOiJTQU1QT1JHIiwic2Vzc2lvbl9vcmdfc3RhdHVzIjoiQUNDUkVESVRFRCIsInNlc3Npb25fdXNlcl9sbmFtZSI6IkJCVExFREhFIDMgLSAxIiwic2Vzc2lvbl91c2VyX2ZuYW1lIjoiZ2xlbm4iLCJzZXNzaW9uX3VzZXJfdXNlcm5hbWUiOiJzYW50b3NAZ21haWwuY29tIiwic2Vzc2lvbl91c2VyX3Bhc3MiOiIxMjMiLCJzZXNzaW9uX3VzZXJfcm9sZSI6Im5vbmUiLCJzZXNzaW9uX2NsYXNzX3llYXIiOiIzIC0gMSJ9', '2021-08-09 11:52:21.438861'),
('zgn06e055uelo6z6a2gdzoa8n4y5a7jn', 'NGU1OGVlZjM2MjYzNTY4NzA5YThhM2Q3ODdlYzM2ODQwMTU3Mjc0NDp7InNlc3Npb25fdXNlcl9pZCI6MSwic2Vzc2lvbl91c2VyX2xuYW1lIjoiYmFsaXphIiwic2Vzc2lvbl91c2VyX2ZuYW1lIjoiZ2xlbm4iLCJzZXNzaW9uX3VzZXJfdXNlcm5hbWUiOiJvc2FzIiwic2Vzc2lvbl91c2VyX3Bhc3MiOiIxMjMiLCJzZXNzaW9uX3VzZXJfcm9sZSI6IkhFQUQgT1NBUyJ9', '2021-07-02 01:23:01.009160');

-- --------------------------------------------------------

--
-- Table structure for table `osassystem_classroom`
--

CREATE TABLE `osassystem_classroom` (
  `room_id` int(11) NOT NULL,
  `room_year` varchar(20) NOT NULL,
  `room_sec` varchar(50) DEFAULT NULL,
  `room_email` varchar(50) NOT NULL,
  `room_pass` varchar(16) NOT NULL,
  `room_status` varchar(10) NOT NULL,
  `room_expiration` date DEFAULT NULL,
  `room_submit_date` date DEFAULT NULL,
  `room_stud_id_id` int(11) DEFAULT NULL,
  `room_datecreated` date NOT NULL,
  `room_dateupdated` date NOT NULL,
  `room_fund` int(11) NOT NULL,
  `room_course` varchar(300) DEFAULT NULL,
  `room_adviser` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `osassystem_concept_paper_title`
--

CREATE TABLE `osassystem_concept_paper_title` (
  `title_id` int(11) NOT NULL,
  `title_name` varchar(200) NOT NULL,
  `title_datecreated` date NOT NULL,
  `title_status` varchar(20) DEFAULT NULL,
  `title_auth_id_id` int(11) DEFAULT NULL,
  `title_org_id_id` int(11) DEFAULT NULL,
  `title_room_id_id` int(11) DEFAULT NULL,
  `title_dateapproved` date DEFAULT NULL,
  `title_accomplishment_file` varchar(100) DEFAULT NULL,
  `title_date_accomplished` date DEFAULT NULL,
  `title_accomplishment_file_ext` varchar(20) DEFAULT NULL,
  `title_serial` varchar(15) DEFAULT NULL,
  `title_date_conducted` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `osassystem_concept_paper_title`
--

INSERT INTO `osassystem_concept_paper_title` (`title_id`, `title_name`, `title_datecreated`, `title_status`, `title_auth_id_id`, `title_org_id_id`, `title_room_id_id`, `title_dateapproved`, `title_accomplishment_file`, `title_date_accomplished`, `title_accomplishment_file_ext`, `title_serial`, `title_date_conducted`) VALUES
(69, 'General Assembly', '2020-11-06', 'ACCOMPLISHED', NULL, 13, NULL, '2020-11-06', 'CommITS-Accomplishment-Report-General-Assembly-Nov23_Dec1.pdf', '2020-12-01', 'pdf', 'SN-C3OE7', '2020-11-23'),
(70, 'Sulong Kababayan Donation Drive', '2020-10-29', 'ACCOMPLISHED', NULL, 13, NULL, '2020-10-29', 'Sulong-kababayan-AR-1.pdf', '2020-11-10', 'pdf', 'SN-EGENK', '2020-11-02'),
(71, 'Lend a Hand Donation Drive', '2020-11-12', 'ACCOMPLISHED', NULL, 13, NULL, '2020-11-12', 'CommitsDonation.AR-converted.pdf', '2020-11-21', 'pdf', 'SN-W7TCT', '2020-11-13'),
(72, 'Freshman Tutorial', '2021-01-05', 'ACCOMPLISHED', NULL, 13, NULL, '2021-01-05', 'CommITS-Accomplishment-Report-C-Programming-LectureJan24_Feb2.docx', '2021-02-02', 'docx', 'SN-UQA08', '2021-01-24'),
(73, 'Traversing I.T. Career Opportunities', '2021-01-05', 'ACCOMPLISHED', NULL, 13, NULL, '2021-01-05', 'CommITS-Accomplishment-Report-Traversing-I.T.-Career-OpportunitiesFeb12_Feb20.docx', '2021-02-20', 'T', 'SN-555VB', '2021-02-12'),
(74, 'Make IT Count: Exploring Java Programming Language in Software Development.', '2021-01-12', 'ACCOMPLISHED', NULL, 13, NULL, '2021-01-12', 'CommITS-Accomplishment-Report-Java-Programming-TutorialMay14_May21.pdf', '2021-05-21', 'pdf', 'SN-GLFGI', '2021-05-14'),
(76, 'This is IT: Interactive Short-Course for Systems Analysis and Design.', '2021-01-12', 'ACCOMPLISHED', NULL, 13, NULL, '2021-01-12', 'CommITS-Accomplishment-Report-Systems-Analysis-and-Design-TutorialApril30_May8.pdf', '2021-05-08', 'pdf', 'SN-9FLQC', '2021-04-30'),
(77, 'Engaging Possibilities: Initiating the Future of I.T. Raising Leaders in a Technological Society.', '2021-01-12', 'ACCOMPLISHED', NULL, 13, NULL, '2021-01-12', 'CommITS-Accomplishment-Report-LeadershipApril17_April25.pdf', '2021-04-25', 'pdf', 'SN-B9HOL', '2021-04-17'),
(78, 'Engaging possibilities : Seizing Success in Business & Technology.', '2021-04-12', 'ACCOMPLISHED', NULL, 13, NULL, '2021-04-12', 'CommITS-Accomplishment-Report-Seizing-SuccessMay29_June7.pdf', '2021-05-29', 'pdf', 'SN-6KI87', '2021-05-24'),
(79, 'IT Share It', '2021-04-12', 'ACCOMPLISHED', NULL, 13, NULL, '2021-04-12', 'CommITS-Accomplishment-Report-Share-ITJune4_June12.pdf', '2021-06-12', 'pdf', 'SN-XL9BK', '2021-06-04'),
(80, 'Health awareness, Digital Literacy, and Enhancing Work Productivity: Towards an Equipped Filipino Worker in the Midst of the Pandemic', '2021-04-16', 'ACCOMPLISHED', NULL, 13, NULL, '2021-04-16', 'May17_July17Accomplishment_Report_Extension_Program-COMMITS_CHRS.pdf', '2021-07-17', 'pdf', 'SN-X7Z0I', '2021-05-17'),
(83, 'JMS MARKFEST: Webinar “Unveiling Diverse Strategies in a Digital Marketing Context”', '2020-11-26', 'ACCOMPLISHED', NULL, 15, NULL, '2020-11-29', 'AR_JMS_MMFF_2021.pdf', '2020-01-24', 'pdf', 'SN-NBOEP', '2020-01-18'),
(85, 'JMS MARKFEST: Obra Marketista “Great Talents Through Digital Contemporary Art”', '2020-11-26', 'ACCOMPLISHED', NULL, 15, NULL, '2020-11-27', 'AR_JMS_OBRA_MARKETISTA_MARKFEST_2021.pdf', '2021-01-30', 'pdf', 'SN-O6RO0', '2021-01-19'),
(86, 'JMS MARKETHINK: “A Basic Guide in Building Wealth Through the Stock Market”', '2021-04-10', 'ACCOMPLISHED', NULL, 15, NULL, '2021-04-10', 'AR_JMS_WEBINAR_MARKETHINK.pdf', '2021-07-30', 'pdf', 'SN-9PZNV', '2021-04-29'),
(87, 'JMS Marketing Management Film Festival 2021 “MMFF 2021: Behind the Scenes”', '2021-05-24', 'ACCOMPLISHED', NULL, 15, NULL, '2021-05-24', 'AR_JMS_MMFF_2021_tBg5nR7.pdf', '2021-06-29', 'pdf', 'SN-BXGKH', '2021-06-24'),
(88, 'Future Proof in Coping Up with the New Trends', '2021-03-05', 'ACCOMPLISHED', NULL, 16, NULL, '2021-04-05', 'AR-_CHRS_1st_Webinar.pdf', '2021-03-14', 'pdf', 'SN-584T1', '2021-03-08'),
(89, 'PUP QC Virtual Career Expo 2021: A Path in the New Normal', '2021-04-05', 'ACCOMPLISHED', NULL, 16, NULL, '2021-04-05', 'AR-_Virtual_Career_Fair_2021.pdf', '2021-05-30', 'pdf', 'SN-BDJU5', '2021-05-24'),
(90, 'Extension Project: Health Awareness, Digital Literacy, and Enhancing Work Productivity: Towards an Equipped Filipino Worker in the Midst of the Pandemic', '2021-04-16', 'ACCOMPLISHED', NULL, 16, NULL, '2021-04-16', 'AR-Extension_Program-COMMITS_CHRS_ZgirpGp.pdf', '2021-05-25', 'pdf', 'SN-GLFD3', '2021-05-17'),
(92, 'Strategic Planning', '2021-02-11', 'ACCOMPLISHED', NULL, 19, NULL, '2021-02-12', 'AR_STRAT_PLANNING_2021.pdf', '2021-02-25', 'pdf', 'SN-BLH4H', '2021-02-16'),
(93, 'Mental Health', '2021-02-28', 'ACCOMPLISHED', NULL, 19, NULL, '2021-02-28', 'AR_Mental_Health.pdf', '2021-03-05', 'pdf', 'SN-AFAX4', '2021-03-01'),
(94, 'Covid-19; Updates and Vaccines', '2021-07-12', 'ACCOMPLISHED', NULL, 19, NULL, '2021-07-12', '_AR_Covid-19_Update_and_Vacinnes.pdf', '2021-07-26', 'pdf', 'SN-NGLHJ', '2021-07-21'),
(95, 'AgriXhibit: Building Our Entre-Pinoy Mindset', '2021-03-23', 'APPROVED', NULL, 20, NULL, '2021-03-23', '', NULL, NULL, 'SN-XSVYW', '2021-06-07'),
(96, 'COVID-19 FORCED BUSINESS TRANSFORMATION: A PHILIPPINES BUSINESS INDUSTRY PIVOTS IN STATE OF FURTUITOUS EVENTS', '2021-05-03', 'ACCOMPLISHED', NULL, 20, NULL, '2021-05-03', 'YES-Webinar-Accomplishment_Report-2021_1.docx', '2021-05-04', 'docx', 'SN-CYLHW', '2021-04-30'),
(97, 'STRATEGIC PLANNING 2021: Puso, Utak, At Adhika; Paninindigan Sa Gampanin Bilang Mga Iskolar Para Sa Bayan', '2021-02-11', 'APPROVED', NULL, 21, NULL, '2021-02-11', '', NULL, NULL, 'SN-RNYHX', '2021-02-11'),
(98, 'WEBINAR AND CONTEST: The 21st Generation Artists and Writers: Challenges Amidst Pandemic', '2021-02-22', 'APPROVED', NULL, 21, NULL, '2021-02-22', '', NULL, NULL, 'SN-OEKES', '2021-03-05'),
(99, 'PUPQC VIRTUAL CAREER EXPO 2021: A Path in the New NormaL', '2021-05-24', 'APPROVED', NULL, 21, NULL, '2021-05-24', '', NULL, NULL, 'SN-I5CE0', '2021-05-25'),
(100, 'Extension Project: Health awareness, Digital Literacy, and enhancing work productivity: towards an equipped Filipino worker in the midst of the pandemic.', '2021-04-16', 'APPROVED', NULL, 21, NULL, '2021-04-17', '', NULL, NULL, 'SN-I4SP0', '2021-05-24'),
(101, 'FBTO Got Talent', '2021-02-15', 'ACCOMPLISHED', NULL, 22, NULL, '2021-02-16', 'FBTO-GOT-TALENT_1.docx', '2021-02-28', 'docx', 'SN-K0496', '2021-02-26'),
(102, 'Mental Health Webinar  &quot;IT’S OK NOT TO BE OK: Dealing with Uncertainty and Anxiety in the New Normal”', '2021-02-24', 'ACCOMPLISHED', NULL, 22, NULL, '2021-02-25', 'FBTO-AR-Webinar-for-Mental-Health.pdf', '2021-03-05', 'pdf', 'SN-KQHIR', '2021-03-01'),
(103, 'YOU MATTER: Nurturing Minds and Hearts', '2021-02-26', 'ACCOMPLISHED', NULL, 22, NULL, '2021-02-27', 'YOU_Matter_Webinar.pdf', '2021-03-10', 'pdf', 'SN-BD03W', '2021-03-05'),
(104, 'Technolympics 2021 “EducXhibition: A Battle of Skills and Innovation of Future Business Educators”', '2021-05-05', 'ACCOMPLISHED', NULL, 22, NULL, '2021-05-06', 'TECHNOLYMPICS.AR_2021.docx', '2021-05-11', 'AR_2021', 'SN-GEKLH', '2021-05-07'),
(105, 'Support E-Iskolar: MLBB Campus Open Tournament', '2021-03-16', 'ACCOMPLISHED', NULL, 24, NULL, '2021-03-16', 'ML-AR.pdf', '2021-05-20', 'pdf', 'SN-5A85A', '2021-05-17'),
(106, 'Health Records and Management of Polytechnic University of the Philippines Quezon City Branch', '2021-06-21', 'ACCOMPLISHED', NULL, 23, NULL, '2021-06-21', 'DOMTCs_Second_Accomplishment.pdf', '2021-06-23', 'pdf', 'SN-OY9DA', '2021-06-21'),
(107, 'Salient Points and Updates on RA No. 10173 otherwise known as the Data Privacy Act of 2012 in relation to  Health Records Management', '2021-06-15', 'ACCOMPLISHED', NULL, 23, NULL, '2021-06-15', 'DOMTCs_First_Accomplishment.pdf', '2021-06-18', 'pdf', 'SN-CCOM2', '2021-06-15');

-- --------------------------------------------------------

--
-- Table structure for table `osassystem_fund`
--

CREATE TABLE `osassystem_fund` (
  `fund_id` int(11) NOT NULL,
  `fund_desc` varchar(500) DEFAULT NULL,
  `fund_amount` int(11) NOT NULL,
  `fund_word` varchar(500) NOT NULL,
  `fund_status` varchar(20) NOT NULL,
  `fund_date_requested` date NOT NULL,
  `fund_date_approved` date DEFAULT NULL,
  `fund_head_id_id` int(11) DEFAULT NULL,
  `fund_org_id_id` int(11) DEFAULT NULL,
  `fund_room_id_id` int(11) DEFAULT NULL,
  `fund_type` varchar(50) DEFAULT NULL,
  `fund_serial` varchar(15) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `osassystem_fund_file`
--

CREATE TABLE `osassystem_fund_file` (
  `fund_f_id` int(11) NOT NULL,
  `fund_f_file` varchar(100) DEFAULT NULL,
  `fund_f_file_ext` varchar(20) DEFAULT NULL,
  `fund_f_status` varchar(20) NOT NULL,
  `fund_f_head_id_id` int(11) DEFAULT NULL,
  `fund_f_org_id_id` int(11) DEFAULT NULL,
  `fund_f_room_id_id` int(11) DEFAULT NULL,
  `fund_fund_id_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `osassystem_officer`
--

CREATE TABLE `osassystem_officer` (
  `off_id` int(11) NOT NULL,
  `off_position` varchar(200) NOT NULL,
  `off_status` varchar(20) NOT NULL,
  `off_date_added` date NOT NULL,
  `off_org_id_id` int(11) DEFAULT NULL,
  `off_room_id_id` int(11) DEFAULT NULL,
  `off_stud_id_id` int(11) DEFAULT NULL,
  `off_signature` varchar(100) DEFAULT NULL,
  `off_signature_ext` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `osassystem_officer`
--

INSERT INTO `osassystem_officer` (`off_id`, `off_position`, `off_status`, `off_date_added`, `off_org_id_id`, `off_room_id_id`, `off_stud_id_id`, `off_signature`, `off_signature_ext`) VALUES
(56, 'President', 'ACTIVE', '2021-07-30', 15, NULL, 19, '', NULL),
(57, 'President', 'ACTIVE', '2021-07-30', 16, NULL, 20, '', NULL),
(61, 'President', 'ACTIVE', '2021-08-01', 19, NULL, 21, '', NULL),
(62, 'President', 'ACTIVE', '2021-08-01', 20, NULL, 22, '', NULL),
(63, 'President', 'ACTIVE', '2021-08-01', 21, NULL, 23, '', NULL),
(64, 'President', 'ACTIVE', '2021-08-01', 22, NULL, 24, '', NULL),
(65, 'President', 'ACTIVE', '2021-08-01', 23, NULL, 25, '', NULL),
(66, 'President', 'ACTIVE', '2021-08-01', 24, NULL, 26, '', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `osassystem_organization`
--

CREATE TABLE `osassystem_organization` (
  `org_id` int(11) NOT NULL,
  `org_name` varchar(50) NOT NULL,
  `org_abbr` varchar(50) DEFAULT NULL,
  `org_email` varchar(50) NOT NULL,
  `org_pass` varchar(16) NOT NULL,
  `org_status` varchar(10) NOT NULL,
  `org_notes` varchar(500) DEFAULT NULL,
  `org_submit_date` date DEFAULT NULL,
  `org_date_accredited` date DEFAULT NULL,
  `org_date_accredited_year` date DEFAULT NULL,
  `org_datecreated` date NOT NULL,
  `org_dateupdated` date NOT NULL,
  `org_expiration` date DEFAULT NULL,
  `org_stud_id_id` int(11) DEFAULT NULL,
  `org_fund` int(11) NOT NULL,
  `org_course` varchar(500) DEFAULT NULL,
  `org_logo` varchar(100) DEFAULT NULL,
  `org_accre_status` int(11) NOT NULL,
  `org_adviser` varchar(50) DEFAULT NULL,
  `org_type` varchar(50) DEFAULT NULL,
  `org_issue` varchar(500) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `osassystem_organization`
--

INSERT INTO `osassystem_organization` (`org_id`, `org_name`, `org_abbr`, `org_email`, `org_pass`, `org_status`, `org_notes`, `org_submit_date`, `org_date_accredited`, `org_date_accredited_year`, `org_datecreated`, `org_dateupdated`, `org_expiration`, `org_stud_id_id`, `org_fund`, `org_course`, `org_logo`, `org_accre_status`, `org_adviser`, `org_type`, `org_issue`) VALUES
(13, 'Commonwealth Information Technology Society', 'COMMITS', 'asilanjrmarkkennedy@gmail.com', '10189213g', 'ACCREDITED', NULL, '2020-10-10', '2020-10-15', '2020-10-15', '2020-10-15', '2020-10-15', '2021-10-15', 18, 0, NULL, '', 1, 'Prof. Alma Fernandez', 'College-Based', NULL),
(15, 'Junior Marketing Society', 'JMS', 'jtrabadon@gmail.com', '123', 'ACCREDITED', NULL, '2020-10-10', '2020-10-15', '2020-10-15', '2020-10-10', '2021-07-30', '2021-10-10', 19, 40, NULL, '', 0, 'Prof. Jhano Isip', 'College-Based', NULL),
(16, 'Community of Human Resource Student', 'CHRS', 'baldovizokristinejoy@gmail.com', '123', 'ACCREDITED', NULL, '2020-10-10', '2020-10-15', '2020-10-15', '2020-10-10', '2021-07-30', '2021-10-10', 20, 0, NULL, '', 0, 'Prof. Melanie Bactasa', 'College-Based', NULL),
(19, 'Supreme Student Council', 'SSC', 'dan.mercado.jr27@gmail.com', '123', 'ACCREDITED', NULL, '2021-08-01', '2021-08-01', '2021-08-01', '2021-08-01', '2021-08-01', '2022-08-01', 21, 0, NULL, '', 1, 'N/A', 'College-Based', NULL),
(20, 'Youth Entrepreneurship Society', 'YES', 'johnricdelosreyes@yahoo.com', '123', 'ACCREDITED', NULL, '2021-08-01', '2021-08-01', '2021-08-01', '2021-08-01', '2021-08-01', '2022-08-01', 22, 0, NULL, '', 1, 'Prof. Rodrigo Dolorosa', 'College-Based', NULL),
(21, 'Vox Nova', 'Vox Nova', 'Caspermorada2000@gmail.com', '123', 'ACCREDITED', NULL, '2021-08-01', '2021-08-01', '2021-08-01', '2021-08-01', '2021-08-01', '2022-08-01', 23, 0, NULL, '', 1, 'Prof. Roseller Malabanan', 'College-Based', NULL),
(22, 'Future business teachers organization', 'FBTO', 'jayann.rom08@gmail.com', '123', 'ACCREDITED', NULL, '2021-08-01', '2021-08-01', '2021-08-01', '2021-08-01', '2021-08-01', '2022-08-01', 24, 0, NULL, '', 1, 'Prof. Caroline T. Sumande', 'College-Based', NULL),
(23, 'Distinguished Organization of Management Technolog', 'DOMTCS', 'kfjacinto@gmail.com', '123', 'ACCREDITED', NULL, '2021-08-01', '2021-08-01', '2021-08-01', '2021-08-01', '2021-08-01', '2022-08-01', 25, 0, NULL, '', 1, 'Prof. Sheryl Morales', 'College-Based', NULL),
(24, 'PUPQC Sports Club', 'PUPQC Sports Club', 'smjfranciak@gmail.com', '123', 'ACCREDITED', NULL, '2021-08-01', '2021-08-01', '2021-08-01', '2021-08-01', '2021-08-01', '2022-08-01', 26, 0, NULL, '', 1, 'Prof. Rommel Roxas', 'College-Based', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `osassystem_organization_chat`
--

CREATE TABLE `osassystem_organization_chat` (
  `msg_id` int(11) NOT NULL,
  `msg_message` varchar(200) NOT NULL,
  `msg_status` varchar(10) NOT NULL,
  `msg_date` datetime(6) NOT NULL,
  `msg_send_to` varchar(200) DEFAULT NULL,
  `msg_send_from` varchar(200) DEFAULT NULL,
  `msg_head_id_id` int(11) DEFAULT NULL,
  `msg_org_id_id` int(11) DEFAULT NULL,
  `msg_room_id_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `osassystem_organization_chat`
--

INSERT INTO `osassystem_organization_chat` (`msg_id`, `msg_message`, `msg_status`, `msg_date`, `msg_send_to`, `msg_send_from`, `msg_head_id_id`, `msg_org_id_id`, `msg_room_id_id`) VALUES
(125, 'sdfsdaf', 'Delivered', '2021-07-29 03:54:13.000000', 'SAMPLE', '1', 1, NULL, NULL),
(126, 'hi', 'Delivered', '2021-07-30 01:47:19.000000', 'COMMITS', '1', 1, NULL, NULL),
(127, 'hey', 'Delivered', '2021-07-30 01:47:26.000000', 'COMMITS', '1', 1, NULL, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `osassystem_org_accreditation`
--

CREATE TABLE `osassystem_org_accreditation` (
  `acc_id` int(11) NOT NULL,
  `acc_title` varchar(200) DEFAULT NULL,
  `acc_file` varchar(100) DEFAULT NULL,
  `acc_return_file` varchar(100) DEFAULT NULL,
  `acc_doc_type` varchar(20) DEFAULT NULL,
  `acc_status` varchar(20) NOT NULL,
  `acc_datecreated` date NOT NULL,
  `acc_dateupdated` date NOT NULL,
  `acc_org_id_id` int(11) DEFAULT NULL,
  `acc_room_id_id` int(11) DEFAULT NULL,
  `acc_docu_term` int(11) DEFAULT NULL,
  `acc_issue` varchar(500) DEFAULT NULL,
  `acc_datesubmitted` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `osassystem_org_accreditation`
--

INSERT INTO `osassystem_org_accreditation` (`acc_id`, `acc_title`, `acc_file`, `acc_return_file`, `acc_doc_type`, `acc_status`, `acc_datecreated`, `acc_dateupdated`, `acc_org_id_id`, `acc_room_id_id`, `acc_docu_term`, `acc_issue`, `acc_datesubmitted`) VALUES
(63, 'Set of Officers', 'commits-Officers-2020-2021_6WqEjQJ.docx', '', 'docx', 'SENT', '2021-07-29', '2021-07-29', 13, NULL, 1, NULL, '2021-07-29'),
(71, 'Registrar Certificate', 'BSIT-Enrolled-Officers.docx', '', 'docx', 'SENT', '2021-07-29', '2021-07-29', 13, NULL, 1, NULL, '2021-07-29'),
(72, 'Plan Activities', 'commits-action-plan.docx', '', 'docx', 'SENT', '2021-07-29', '2021-07-29', 13, NULL, 1, NULL, '2021-07-29'),
(73, 'New Constitution', 'proposedcbl-1_1.docx', '', 'docx', 'SENT', '2021-07-29', '2021-07-29', 13, NULL, 1, NULL, '2021-07-29'),
(74, 'Guidance Certificate', 'MH-Declaration-2020-Cert-COMMITS.pdf', '', 'pdf', 'SENT', '2021-07-29', '2021-07-29', 13, NULL, 1, NULL, '2021-07-29'),
(75, 'Annual Report', 'CommITS-AR-2019-2020.pdf', '', 'pdf', 'SENT', '2021-07-29', '2021-07-29', 13, NULL, 1, NULL, '2021-07-29');

-- --------------------------------------------------------

--
-- Table structure for table `osassystem_org_concept_paper`
--

CREATE TABLE `osassystem_org_concept_paper` (
  `con_id` int(11) NOT NULL,
  `con_file` varchar(100) DEFAULT NULL,
  `con_file_ext` varchar(20) DEFAULT NULL,
  `con_status` varchar(20) NOT NULL,
  `con_datecreated` date NOT NULL,
  `con_dateupdated` date NOT NULL,
  `con_title_id_id` int(11) DEFAULT NULL,
  `con_auth_id_id` int(11) DEFAULT NULL,
  `con_org_id_id` int(11) DEFAULT NULL,
  `con_room_id_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `osassystem_org_concept_paper`
--

INSERT INTO `osassystem_org_concept_paper` (`con_id`, `con_file`, `con_file_ext`, `con_status`, `con_datecreated`, `con_dateupdated`, `con_title_id_id`, `con_auth_id_id`, `con_org_id_id`, `con_room_id_id`) VALUES
(139, 'concept-paper-request.docx', 'docx', 'APPROVED', '2020-11-06', '2020-11-06', 69, 1, 13, NULL),
(140, 'COMMITS-CONCEPT-PAPER-G.a.docx', 'docx', 'APPROVED', '2020-11-06', '2020-11-06', 69, 1, 13, NULL),
(142, 'concept-paper-request-Sulong-Kababayan.docx', 'docx', 'APPROVED', '2021-07-29', '2021-07-29', 70, 1, 13, NULL),
(144, 'concept-paper-request-Lend-a-hand.docx', 'docx', 'APPROVED', '2021-07-29', '2021-07-29', 71, 1, 13, NULL),
(146, 'COMMITS-CONCEPT-PAPER-freshman-tutorial.docx', 'docx', 'APPROVED', '2021-07-29', '2021-07-29', 72, 1, 13, NULL),
(149, 'concept-paper-request-IT-CAREER.docx', 'docx', 'APPROVED', '2021-07-29', '2021-07-29', 73, 1, 13, NULL),
(150, 'COMMITS-CONCEPT-PAPER-IT-Career.docx', 'docx', 'APPROVED', '2021-07-29', '2021-07-29', 73, 1, 13, NULL),
(155, 'COMMITS-CONCEPT-PAPER-2nd-tutorial-java.docx', 'docx', 'APPROVED', '2021-07-29', '2021-07-29', 74, 1, 13, NULL),
(156, 'concept-paper-request-2nd-tutorial.docx', 'docx', 'APPROVED', '2021-07-29', '2021-07-29', 74, 1, 13, NULL),
(157, 'concept-paper-request-3rd-tutorial.docx', 'docx', 'APPROVED', '2021-07-29', '2021-07-29', 76, 1, 13, NULL),
(160, 'concept-paper-request-Leadership.docx', 'docx', 'APPROVED', '2021-07-29', '2021-07-29', 77, 1, 13, NULL),
(161, 'COMMITS-CONCEPT-PAPER-leadership.docx', 'docx', 'APPROVED', '2021-07-29', '2021-07-29', 77, 1, 13, NULL),
(164, 'concept-paper-request-business.docx', 'docx', 'APPROVED', '2021-07-29', '2021-07-29', 78, 1, 13, NULL),
(165, 'COMMITS-CONCEPT-PAPER-business_1.docx', 'docx', 'APPROVED', '2021-07-29', '2021-07-29', 78, 1, 13, NULL),
(168, 'COMMITS-CONCEPT-PAPER-contest.docx', 'docx', 'APPROVED', '2021-07-29', '2021-07-29', 79, 1, 13, NULL),
(169, 'concept-paper-request-Contest.docx', 'docx', 'APPROVED', '2021-07-29', '2021-07-29', 79, 1, 13, NULL),
(172, 'concept-paper-request-extension-updated.docx', 'docx', 'APPROVED', '2021-07-30', '2021-07-30', 80, 1, 13, NULL),
(173, 'COMMITS_CONCEPT_PAPER_extensionupdated.docx', 'docx', 'APPROVED', '2021-07-30', '2021-07-30', 80, 1, 13, NULL),
(176, 'CP_JMS_MMFF_2021.pdf', 'pdf', 'SENT', '2021-07-30', '2021-07-30', 83, NULL, 15, NULL),
(177, 'SIGNED_LETTER_JMS_MMFF_2021.pdf', 'pdf', 'APPROVED', '2021-07-30', '2021-07-30', 83, 1, 15, NULL),
(180, 'CP_JMS_OBRA_MARKETISTA_MARKFEST_2021.pdf', 'pdf', 'SENT', '2021-07-30', '2021-07-30', 85, NULL, 15, NULL),
(183, 'SIGNED_LETTER_JMS_OBRA_MARKETISTA_MARKFEST_2021.pdf', 'pdf', 'SENT', '2021-07-30', '2021-07-30', 85, NULL, 15, NULL),
(185, 'SIGNED_LETTER_JMS_OBRA_MARKETISTA_MARKFEST_2021_OZbtes1.pdf', 'pdf', 'APPROVED', '2021-07-30', '2021-07-30', 85, 1, 15, NULL),
(186, 'CP_JMS_WEBINAR_MARKETHINK.pdf', 'pdf', 'SENT', '2021-07-30', '2021-07-30', 86, NULL, 15, NULL),
(187, 'SIGNED_LETTER_JMS_WEBINAR_MARKETHINK.pdf', 'pdf', 'SENT', '2021-07-30', '2021-07-30', 86, NULL, 15, NULL),
(188, 'SIGNED_LETTER_JMS_WEBINAR_MARKETHINK_P9FHSKu.pdf', 'pdf', 'APPROVED', '2021-07-30', '2021-07-30', 86, 1, 15, NULL),
(189, 'CP_JMS_WEBINAR_MARKFEST_2021.pdf', 'pdf', 'SENT', '2021-07-30', '2021-07-30', 87, NULL, 15, NULL),
(190, 'SIGNED_LETTER_JMS_WEBINAR_MARKFEST_2021.pdf', 'pdf', 'APPROVED', '2021-07-30', '2021-07-30', 87, 1, 15, NULL),
(191, 'CP-_CHRS_1st_Webinar.docx', 'docx', 'SENT', '2021-07-30', '2021-07-30', 88, NULL, 16, NULL),
(192, 'CHRS-1st-Webinar-Approval.docx', 'docx', 'APPROVED', '2021-07-30', '2021-07-30', 88, 1, 16, NULL),
(193, 'CP-_Virtual_Career_Fair_2021.docx', 'docx', 'SENT', '2021-07-30', '2021-07-30', 89, NULL, 16, NULL),
(194, 'CP-_Virtual_Career_Fair_2021.pdf', 'pdf', 'SENT', '2021-07-30', '2021-07-30', 89, NULL, 16, NULL),
(195, 'Request_Letter_-_Virtual_Job_Fair.docx', 'docx', 'APPROVED', '2021-07-30', '2021-07-30', 89, 1, 16, NULL),
(196, 'CHRS_Extension_with_COMMITS.docx', 'docx', 'SENT', '2021-07-30', '2021-07-30', 90, NULL, 16, NULL),
(197, 'CHRS_Extension_with_COMMITS_hggeenA.docx', 'docx', 'APPROVED', '2021-07-30', '2021-07-30', 90, 1, 16, NULL),
(198, 'AR-Extension_Program-COMMITS_CHRS.pdf', 'pdf', 'SENT', '2021-07-30', '2021-07-30', 90, NULL, 16, NULL),
(201, 'PUPQC-COL-Strat-Planning-2021.pdf', 'pdf', 'SENT', '2021-08-01', '2021-08-01', 92, NULL, 19, NULL),
(202, 'Communication_Letter.jpg', 'jpg', 'APPROVED', '2021-08-01', '2021-08-01', 92, 1, 19, NULL),
(203, '_Concept-Paper-Mental-Health-Webinar-.pdf', 'pdf', 'SENT', '2021-08-01', '2021-08-01', 93, NULL, 19, NULL),
(204, 'Communication-Letter-Mental-Health-Webinar-.pdf', 'pdf', 'APPROVED', '2021-08-01', '2021-08-01', 93, 1, 19, NULL),
(205, '_Concept_Paper_Covid-19_Updates_Vaccines.pdf', 'pdf', 'SENT', '2021-08-01', '2021-08-01', 94, NULL, 19, NULL),
(206, 'Communication_Letter_-_CoVid_Update.jpg', 'jpg', 'APPROVED', '2021-08-01', '2021-08-01', 94, 1, 19, NULL),
(207, 'YES-Innovation-Concept-Paper-2021-1.docx', 'docx', 'SENT', '2021-08-01', '2021-08-01', 95, NULL, 20, NULL),
(208, 'YES-Letter-to-the-Admin-Exhibit_2021.docx', 'docx', 'APPROVED', '2021-08-01', '2021-08-01', 95, 1, 20, NULL),
(209, 'YES-Webinar-Concept-paper-2021.docx', 'docx', 'SENT', '2021-08-01', '2021-08-01', 96, NULL, 20, NULL),
(210, 'YES-Webinar-Budgetary_Outlay-2021.docx', 'docx', 'SENT', '2021-08-01', '2021-08-01', 96, NULL, 20, NULL),
(211, 'YES-Letter-to-the-Admin-Webinar_2021.docx', 'docx', 'APPROVED', '2021-08-01', '2021-08-01', 96, 1, 20, NULL),
(212, 'PUPQC-COL-Strat-Planning-2021_ks9pYwT.pdf', 'pdf', 'SENT', '2021-08-01', '2021-08-01', 97, NULL, 21, NULL),
(213, 'Request_Letter_-_Strat_Plan.jpg', 'jpg', 'APPROVED', '2021-08-01', '2021-08-01', 97, 1, 21, NULL),
(214, 'Request_Letter_-_WebinarContest.pdf', 'pdf', 'SENT', '2021-08-01', '2021-08-01', 98, NULL, 21, NULL),
(215, 'ORIGINAL_CONCEPT_PAPER.docx', 'docx', 'SENT', '2021-08-01', '2021-08-01', 98, NULL, 21, NULL),
(216, 'APPROVED_CONCEPT_PAPER.docx', 'docx', 'APPROVED', '2021-08-01', '2021-08-01', 98, 1, 21, NULL),
(217, 'APPROVED_C.P_JOB_FAIR.pdf', 'P (JOB FAIR)', 'SENT', '2021-08-01', '2021-08-01', 99, NULL, 21, NULL),
(218, 'Request_Letter_-_Job_Fair.pdf', 'pdf', 'SENT', '2021-08-01', '2021-08-01', 99, NULL, 21, NULL),
(219, 'APPROVED_C.P_JOB_FAIR_U42JwTk.pdf', 'P (JOB FAIR)', 'APPROVED', '2021-08-01', '2021-08-01', 99, 1, 21, NULL),
(220, 'Concept_Paper_-_Extension_Program.pdf', 'pdf', 'SENT', '2021-08-01', '2021-08-01', 100, NULL, 21, NULL),
(221, 'Request_Letter_-_Extension_Program.pdf', 'pdf', 'APPROVED', '2021-08-01', '2021-08-01', 100, 1, 21, NULL),
(222, 'CP_FBTO-Got-Talent.pdf', 'pdf', 'SENT', '2021-08-01', '2021-08-01', 101, NULL, 22, NULL),
(223, 'CP_FBTO-Got-Talent_BbgAgD6.pdf', 'pdf', 'APPROVED', '2021-08-01', '2021-08-01', 101, 1, 22, NULL),
(224, 'CP_Mental-Health-Webinar-FBTO-2021-2.pdf', 'pdf', 'SENT', '2021-08-01', '2021-08-01', 102, NULL, 22, NULL),
(225, 'CP_Mental-Health-Webinar-FBTO-2021-2_IisP2eL.pdf', 'pdf', 'APPROVED', '2021-08-01', '2021-08-01', 102, 1, 22, NULL),
(227, 'Webinar.pdf', 'pdf', 'APPROVED', '2021-08-01', '2021-08-01', 103, 1, 22, NULL),
(229, 'Concept-Paper-Technolympics-2021.docx', 'docx', 'APPROVED', '2021-08-01', '2021-08-01', 104, 1, 22, NULL),
(230, 'ML-Tournament_Concept-Paper-FINAL.pdf', 'pdf', 'SENT', '2021-08-01', '2021-08-01', 105, NULL, 24, NULL),
(231, 'Proposal_LetterLPylonEsports.docx', 'docx', 'APPROVED', '2021-08-01', '2021-08-01', 105, 1, 24, NULL),
(232, 'DOMTCs_Concept_paper_webinar2_1.pdf', 'pdf', 'SENT', '2021-08-01', '2021-08-01', 106, NULL, 23, NULL),
(233, 'Letters_for_the_Admin_2_1.pdf', 'pdf', 'APPROVED', '2021-08-01', '2021-08-01', 106, 1, 23, NULL),
(234, 'DOMTCs_Concept_paper_webinar1.pdf', 'pdf', 'SENT', '2021-08-01', '2021-08-01', 107, NULL, 23, NULL),
(235, 'Letters_for_the_Admin_1.pdf', 'pdf', 'APPROVED', '2021-08-01', '2021-08-01', 107, 1, 23, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `osassystem_osas_r_auth_user`
--

CREATE TABLE `osassystem_osas_r_auth_user` (
  `auth_id` int(11) NOT NULL,
  `auth_lname` varchar(50) NOT NULL,
  `auth_fname` varchar(50) NOT NULL,
  `auth_username` varchar(50) NOT NULL,
  `auth_password` varchar(16) NOT NULL,
  `date_created` date NOT NULL,
  `date_updated` date NOT NULL,
  `auth_status` varchar(10) NOT NULL,
  `auth_role_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `osassystem_osas_r_auth_user`
--

INSERT INTO `osassystem_osas_r_auth_user` (`auth_id`, `auth_lname`, `auth_fname`, `auth_username`, `auth_password`, `date_created`, `date_updated`, `auth_status`, `auth_role_id`) VALUES
(1, 'baliza', 'glenn', 'osas', '1234', '2021-05-06', '2021-05-06', 'ACTIVE', 1);

-- --------------------------------------------------------

--
-- Table structure for table `osassystem_osas_r_course`
--

CREATE TABLE `osassystem_osas_r_course` (
  `course_id` int(11) NOT NULL,
  `course_code` varchar(50) NOT NULL,
  `course_name` varchar(250) NOT NULL,
  `course_add_date` datetime(6) NOT NULL,
  `course_edit_date` date NOT NULL,
  `course_status` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `osassystem_osas_r_course`
--

INSERT INTO `osassystem_osas_r_course` (`course_id`, `course_code`, `course_name`, `course_add_date`, `course_edit_date`, `course_status`) VALUES
(1, 'BBTLEDHE', 'BBTLEDHE', '2021-05-06 00:00:00.000000', '2021-05-06', 'ACTIVE'),
(2, 'DOMTMOM', 'DOMTMOM', '2021-05-06 00:00:00.000000', '2021-05-06', 'ACTIVE'),
(3, 'BSENTREP', 'BSENTREP', '2021-05-06 00:00:00.000000', '2021-05-06', 'ACTIVE'),
(4, 'BSBAHRM', 'BSBAHRM', '2021-05-06 00:00:00.000000', '2021-05-06', 'ACTIVE'),
(5, 'BSBA-MM', 'BSBA-MM', '2021-05-06 00:00:00.000000', '2021-05-06', 'ACTIVE'),
(6, 'BSIT', 'BSIT', '2021-05-06 00:00:00.000000', '2021-05-06', 'ACTIVE');

-- --------------------------------------------------------

--
-- Table structure for table `osassystem_osas_r_personal_info`
--

CREATE TABLE `osassystem_osas_r_personal_info` (
  `stud_id` int(11) NOT NULL,
  `stud_no` varchar(15) NOT NULL,
  `stud_lname` varchar(50) NOT NULL,
  `stud_fname` varchar(50) NOT NULL,
  `stud_mname` varchar(50) NOT NULL,
  `stud_sname` varchar(50) DEFAULT NULL,
  `stud_birthdate` date NOT NULL,
  `stud_gender` varchar(10) NOT NULL,
  `stud_address` varchar(50) NOT NULL,
  `stud_email` varchar(50) NOT NULL,
  `stud_m_number` bigint(20) NOT NULL,
  `stud_hs` varchar(50) NOT NULL,
  `stud_hs_add` varchar(50) NOT NULL,
  `stud_sh` varchar(50) NOT NULL,
  `stud_sh_add` varchar(50) NOT NULL,
  `stud_e_name` varchar(50) NOT NULL,
  `stud_e_address` varchar(50) NOT NULL,
  `stud_e_m_number` bigint(20) NOT NULL,
  `s_password` varchar(16) NOT NULL,
  `date_created` datetime(6) NOT NULL,
  `date_updated` datetime(6) NOT NULL,
  `stud_status` varchar(10) NOT NULL,
  `stud_course_id_id` int(11) NOT NULL,
  `stud_role_id` int(11) DEFAULT NULL,
  `stud_yas_id_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `osassystem_osas_r_personal_info`
--

INSERT INTO `osassystem_osas_r_personal_info` (`stud_id`, `stud_no`, `stud_lname`, `stud_fname`, `stud_mname`, `stud_sname`, `stud_birthdate`, `stud_gender`, `stud_address`, `stud_email`, `stud_m_number`, `stud_hs`, `stud_hs_add`, `stud_sh`, `stud_sh_add`, `stud_e_name`, `stud_e_address`, `stud_e_m_number`, `s_password`, `date_created`, `date_updated`, `stud_status`, `stud_course_id_id`, `stud_role_id`, `stud_yas_id_id`) VALUES
(18, '2017-00308-CM-0', 'ASILAN', 'MARK KENNEDY', 'S.', 'JR', '1993-10-20', 'Male', '79 B STO NINO STREET BRGY HOLY SPIRIT QC HOLYSPIRI', 'asilanjrmarkkennedy@gmail.com', 9207428147, 'HOLYSPIRIT NATIONAL HIGH SCHOOL', 'HOLY SPIRIT', 'N/A', 'N/A', 'JOCELYN ASILAN', '79 B STO NINO STREET BRGY HOLY SPIRIT QC HOLYSPIRI', 9207428147, '123', '2021-07-28 16:34:23.176197', '2021-07-28 07:31:37.364895', 'ACTIVE', 6, 2, 1),
(19, '2017-00046-CM-0', 'RABADON', 'JOMEL', 'R.', '', '1998-07-20', 'Male', 'N/A', 'jtrabadon@gmail.com', 9123456789, 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 9123456789, '123', '2021-07-30 11:37:38.124304', '2021-07-30 11:38:03.530249', 'ACTIVE', 5, 2, 1),
(20, '2018-00295-CM-0', 'BALDOVIZO', 'KRYSTINE JOY', 'NAVARRETE', '', '1999-05-19', 'Female', '103 Steve Street Brgy. Commonwealth, Quezon City', 'baldovizokristinejoy@gmail.com', 9179046290, 'Commonwealth High School', 'Ecol Street Brgy. Commonwealth, Quezon City', 'Polytechnic University of the Philippines', 'Don Fabian Street, Brgy. Commonwealth, Quezon City', 'Mila Baldovizo', '103 Steve Street Brgy. Commonwealth, Quezon City', 9238478844, '123', '2021-07-30 19:11:59.625147', '2021-07-30 11:05:49.329404', 'ACTIVE', 4, 2, 2),
(21, '2017-00300-CM-0', 'MERCADO', 'DANILO', 'S.', 'JR', '1989-10-27', 'Male', 'N/A', 'dan.mercado.jr27@gmail.com', 9777251630, 'Calumpit National High School', 'Calumpang Calumpit Bulacan', 'N/A', 'N/A', 'Rev. Leonard T. Armas', 'N/A', 286459266, '123', '2021-08-01 11:22:31.531913', '2021-08-01 03:11:40.397340', 'ACTIVE', 1, 2, 1),
(22, '2018-00365-CM-0', 'DELOS REYES', 'JOHNRIC', 'PAGAYANAN', '', '1998-04-26', 'Male', '45 ipil ipil street Payatas B. Quezon City', 'johnricdelosreyes@yahoo.com', 9388272013, 'Justice Cecilia munoz palma high school', 'Molave street payatas B.', 'Polytechnic University of the Philippines', 'Don fabian street commonwealth Quezon City', 'Norma delos reyes', '45 ipil ipil street Payatas B. Quezon City', 9224336969, '123', '2021-08-01 11:49:17.119419', '2021-08-01 03:11:40.397340', 'ACTIVE', 3, 2, 3),
(23, '2019-00205-CM-0', 'MORADA', 'JOHN CASPER', 'DEMONTEVERDE', '', '1998-09-20', 'Male', 'Quezon city', 'Caspermorada2000@gmail.com', 9615373232, 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 9615373232, '123', '2021-08-01 12:19:10.870464', '2021-08-01 03:11:40.397340', 'ACTIVE', 1, 2, 4),
(24, '2017-00320-CM-0', 'ROM', 'JAY ANN', 'F.', '', '1997-02-04', 'Female', 'N/A', 'jayann.rom08@gmail.com', 9659451434, 'Biliran Tucdao National High School', 'Tucdao, Kawayan, Biliran', 'N/A', 'N/A', 'Jomari Mosuela', 'N/A', 9087520849, '123', '2021-08-01 13:01:46.424852', '2021-08-01 04:41:42.030024', 'ACTIVE', 1, 2, 1),
(25, '2018-00375-CM-0', 'JACINTO', 'KAREN FAITH', 'SINGZON', '', '1998-09-30', 'Female', 'Blk 6 L137 Southville 8C San Isidro Montalban Rodr', 'kfjacinto@gmail.com', 9302941166, 'KASIGLAHAN VILLAGE NATIONAL HIGH SCHOOL ', 'Kasiglahan Village Rodriguez, Rizal', 'STI College Fairview', 'Regalado Fairview Quezon City', 'Mary Jane S. Jacinto', 'Blk 6 L137 Southville 8C San Isidro Montalban Rodr', 9298121985, '123', '2021-08-01 13:18:43.657916', '2021-08-01 04:41:42.030024', 'ACTIVE', 2, 2, 2),
(26, '2018-00500-CM-0', 'FRANCIA', 'SHIENA MAE JOAN', 'ONREJAS', '', '2000-06-25', 'Female', 'Blk 16 Lot 2 St. Michael Villa Nova Subdivision Br', 'smjfranciak@gmail.com', 9999452289, 'N/A', 'N/A', 'N/A', 'N/A', 'Margie O. Francia', 'Blk 16 Lot 2 St. Michael Villa Nova Subdivision Br', 9275144739, '123', '2021-08-01 13:23:26.705504', '2021-08-01 04:41:42.030024', 'ACTIVE', 4, 2, 2);

-- --------------------------------------------------------

--
-- Table structure for table `osassystem_osas_r_section_and_year`
--

CREATE TABLE `osassystem_osas_r_section_and_year` (
  `yas_id` int(11) NOT NULL,
  `yas_descriptions` varchar(250) NOT NULL,
  `yas_dateregistered` date NOT NULL,
  `status` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `osassystem_osas_r_section_and_year`
--

INSERT INTO `osassystem_osas_r_section_and_year` (`yas_id`, `yas_descriptions`, `yas_dateregistered`, `status`) VALUES
(1, '4 - 1', '2021-05-06', 'ACTIVE'),
(2, '3 - 1', '2021-06-11', 'ACTIVE'),
(3, '3 - 2', '2021-08-01', 'ACTIVE'),
(4, '2 - 1', '2021-08-01', 'ACTIVE');

-- --------------------------------------------------------

--
-- Table structure for table `osassystem_osas_r_userrole`
--

CREATE TABLE `osassystem_osas_r_userrole` (
  `user_id` int(11) NOT NULL,
  `user_type` varchar(50) NOT NULL,
  `date_created` date NOT NULL,
  `date_updated` date NOT NULL,
  `s_image` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `osassystem_osas_r_userrole`
--

INSERT INTO `osassystem_osas_r_userrole` (`user_id`, `user_type`, `date_created`, `date_updated`, `s_image`) VALUES
(1, 'HEAD OSAS', '2021-05-06', '0000-00-00', ''),
(2, 'STUDENT', '2021-05-06', '2021-05-06', 'proof_pic/image.jpg'),
(3, 'OSAS STAFF', '2021-06-11', '2021-06-11', 'proof_pic/image.jpg');

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
-- Indexes for table `osassystem_classroom`
--
ALTER TABLE `osassystem_classroom`
  ADD PRIMARY KEY (`room_id`),
  ADD KEY `OsasSystem_classroom_room_stud_id_id_ec3ab53e_fk_OsasSyste` (`room_stud_id_id`);

--
-- Indexes for table `osassystem_concept_paper_title`
--
ALTER TABLE `osassystem_concept_paper_title`
  ADD PRIMARY KEY (`title_id`),
  ADD UNIQUE KEY `OsasSystem_concept_paper_title_title_name_211ad12f_uniq` (`title_name`),
  ADD UNIQUE KEY `title_serial` (`title_serial`),
  ADD KEY `OsasSystem_concept_p_title_auth_id_id_e4215002_fk_OsasSyste` (`title_auth_id_id`),
  ADD KEY `OsasSystem_concept_p_title_org_id_id_1cbd0a82_fk_OsasSyste` (`title_org_id_id`),
  ADD KEY `OsasSystem_concept_p_title_room_id_id_ed4cc098_fk_OsasSyste` (`title_room_id_id`);

--
-- Indexes for table `osassystem_fund`
--
ALTER TABLE `osassystem_fund`
  ADD PRIMARY KEY (`fund_id`),
  ADD UNIQUE KEY `fund_serial` (`fund_serial`),
  ADD KEY `OsasSystem_fund_fund_head_id_id_4e40d210_fk_OsasSyste` (`fund_head_id_id`),
  ADD KEY `OsasSystem_fund_fund_org_id_id_e550d0d3_fk_OsasSyste` (`fund_org_id_id`),
  ADD KEY `OsasSystem_fund_fund_room_id_id_539a3380_fk_OsasSyste` (`fund_room_id_id`);

--
-- Indexes for table `osassystem_fund_file`
--
ALTER TABLE `osassystem_fund_file`
  ADD PRIMARY KEY (`fund_f_id`),
  ADD KEY `OsasSystem_fund_file_fund_f_head_id_id_bb7a7265_fk_OsasSyste` (`fund_f_head_id_id`),
  ADD KEY `OsasSystem_fund_file_fund_f_org_id_id_c972d039_fk_OsasSyste` (`fund_f_org_id_id`),
  ADD KEY `OsasSystem_fund_file_fund_f_room_id_id_8b934bbe_fk_OsasSyste` (`fund_f_room_id_id`),
  ADD KEY `OsasSystem_fund_file_fund_fund_id_id_d2792c51_fk_OsasSyste` (`fund_fund_id_id`);

--
-- Indexes for table `osassystem_officer`
--
ALTER TABLE `osassystem_officer`
  ADD PRIMARY KEY (`off_id`),
  ADD KEY `OsasSystem_officer_off_org_id_id_2f9acc44_fk_OsasSyste` (`off_org_id_id`),
  ADD KEY `OsasSystem_officer_off_room_id_id_ab7dd79a_fk_OsasSyste` (`off_room_id_id`),
  ADD KEY `OsasSystem_officer_off_stud_id_id_ff19ce3c_fk_OsasSyste` (`off_stud_id_id`);

--
-- Indexes for table `osassystem_organization`
--
ALTER TABLE `osassystem_organization`
  ADD PRIMARY KEY (`org_id`),
  ADD UNIQUE KEY `org_name` (`org_name`),
  ADD KEY `OsasSystem_organizat_org_stud_id_id_1ad0193d_fk_OsasSyste` (`org_stud_id_id`);

--
-- Indexes for table `osassystem_organization_chat`
--
ALTER TABLE `osassystem_organization_chat`
  ADD PRIMARY KEY (`msg_id`),
  ADD KEY `OsasSystem_organizat_msg_head_id_id_1205b0ea_fk_OsasSyste` (`msg_head_id_id`),
  ADD KEY `OsasSystem_organizat_msg_org_id_id_6d62a5a4_fk_OsasSyste` (`msg_org_id_id`),
  ADD KEY `OsasSystem_organizat_msg_room_id_id_585d9efb_fk_OsasSyste` (`msg_room_id_id`);

--
-- Indexes for table `osassystem_org_accreditation`
--
ALTER TABLE `osassystem_org_accreditation`
  ADD PRIMARY KEY (`acc_id`),
  ADD KEY `OsasSystem_org_accre_acc_org_id_id_c1227b3e_fk_OsasSyste` (`acc_org_id_id`),
  ADD KEY `OsasSystem_org_accre_acc_room_id_id_87138f7a_fk_OsasSyste` (`acc_room_id_id`);

--
-- Indexes for table `osassystem_org_concept_paper`
--
ALTER TABLE `osassystem_org_concept_paper`
  ADD PRIMARY KEY (`con_id`),
  ADD KEY `OsasSystem_org_conce_con_title_id_id_d6808307_fk_OsasSyste` (`con_title_id_id`),
  ADD KEY `OsasSystem_org_conce_con_auth_id_id_3aa6e1d7_fk_OsasSyste` (`con_auth_id_id`),
  ADD KEY `OsasSystem_org_conce_con_org_id_id_94587bee_fk_OsasSyste` (`con_org_id_id`),
  ADD KEY `OsasSystem_org_conce_con_room_id_id_a971f8b0_fk_OsasSyste` (`con_room_id_id`);

--
-- Indexes for table `osassystem_osas_r_auth_user`
--
ALTER TABLE `osassystem_osas_r_auth_user`
  ADD PRIMARY KEY (`auth_id`),
  ADD KEY `OsasSystem_osas_r_au_auth_role_id_a2af70fe_fk_OsasSyste` (`auth_role_id`);

--
-- Indexes for table `osassystem_osas_r_course`
--
ALTER TABLE `osassystem_osas_r_course`
  ADD PRIMARY KEY (`course_id`);

--
-- Indexes for table `osassystem_osas_r_personal_info`
--
ALTER TABLE `osassystem_osas_r_personal_info`
  ADD PRIMARY KEY (`stud_id`),
  ADD UNIQUE KEY `stud_no` (`stud_no`),
  ADD KEY `OsasSystem_osas_r_pe_stud_role_id_355f9550_fk_OsasSyste` (`stud_role_id`),
  ADD KEY `OsasSystem_osas_r_pe_stud_yas_id_id_f11e0003_fk_OsasSyste` (`stud_yas_id_id`),
  ADD KEY `OsasSystem_osas_r_pe_stud_course_id_id_891f0471_fk_OsasSyste` (`stud_course_id_id`);

--
-- Indexes for table `osassystem_osas_r_section_and_year`
--
ALTER TABLE `osassystem_osas_r_section_and_year`
  ADD PRIMARY KEY (`yas_id`);

--
-- Indexes for table `osassystem_osas_r_userrole`
--
ALTER TABLE `osassystem_osas_r_userrole`
  ADD PRIMARY KEY (`user_id`);

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
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=117;

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
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=30;

--
-- AUTO_INCREMENT for table `django_migrations`
--
ALTER TABLE `django_migrations`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=78;

--
-- AUTO_INCREMENT for table `osassystem_classroom`
--
ALTER TABLE `osassystem_classroom`
  MODIFY `room_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=34;

--
-- AUTO_INCREMENT for table `osassystem_concept_paper_title`
--
ALTER TABLE `osassystem_concept_paper_title`
  MODIFY `title_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=108;

--
-- AUTO_INCREMENT for table `osassystem_fund`
--
ALTER TABLE `osassystem_fund`
  MODIFY `fund_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=46;

--
-- AUTO_INCREMENT for table `osassystem_fund_file`
--
ALTER TABLE `osassystem_fund_file`
  MODIFY `fund_f_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=38;

--
-- AUTO_INCREMENT for table `osassystem_officer`
--
ALTER TABLE `osassystem_officer`
  MODIFY `off_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=69;

--
-- AUTO_INCREMENT for table `osassystem_organization`
--
ALTER TABLE `osassystem_organization`
  MODIFY `org_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=25;

--
-- AUTO_INCREMENT for table `osassystem_organization_chat`
--
ALTER TABLE `osassystem_organization_chat`
  MODIFY `msg_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=128;

--
-- AUTO_INCREMENT for table `osassystem_org_accreditation`
--
ALTER TABLE `osassystem_org_accreditation`
  MODIFY `acc_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=79;

--
-- AUTO_INCREMENT for table `osassystem_org_concept_paper`
--
ALTER TABLE `osassystem_org_concept_paper`
  MODIFY `con_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=236;

--
-- AUTO_INCREMENT for table `osassystem_osas_r_auth_user`
--
ALTER TABLE `osassystem_osas_r_auth_user`
  MODIFY `auth_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `osassystem_osas_r_course`
--
ALTER TABLE `osassystem_osas_r_course`
  MODIFY `course_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `osassystem_osas_r_personal_info`
--
ALTER TABLE `osassystem_osas_r_personal_info`
  MODIFY `stud_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=27;

--
-- AUTO_INCREMENT for table `osassystem_osas_r_section_and_year`
--
ALTER TABLE `osassystem_osas_r_section_and_year`
  MODIFY `yas_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `osassystem_osas_r_userrole`
--
ALTER TABLE `osassystem_osas_r_userrole`
  MODIFY `user_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

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
-- Constraints for table `osassystem_classroom`
--
ALTER TABLE `osassystem_classroom`
  ADD CONSTRAINT `OsasSystem_classroom_room_stud_id_id_ec3ab53e_fk_OsasSyste` FOREIGN KEY (`room_stud_id_id`) REFERENCES `osassystem_osas_r_personal_info` (`stud_id`);

--
-- Constraints for table `osassystem_concept_paper_title`
--
ALTER TABLE `osassystem_concept_paper_title`
  ADD CONSTRAINT `OsasSystem_concept_p_title_auth_id_id_e4215002_fk_OsasSyste` FOREIGN KEY (`title_auth_id_id`) REFERENCES `osassystem_osas_r_auth_user` (`auth_id`),
  ADD CONSTRAINT `OsasSystem_concept_p_title_org_id_id_1cbd0a82_fk_OsasSyste` FOREIGN KEY (`title_org_id_id`) REFERENCES `osassystem_organization` (`org_id`),
  ADD CONSTRAINT `OsasSystem_concept_p_title_room_id_id_ed4cc098_fk_OsasSyste` FOREIGN KEY (`title_room_id_id`) REFERENCES `osassystem_classroom` (`room_id`);

--
-- Constraints for table `osassystem_fund`
--
ALTER TABLE `osassystem_fund`
  ADD CONSTRAINT `OsasSystem_fund_fund_head_id_id_4e40d210_fk_OsasSyste` FOREIGN KEY (`fund_head_id_id`) REFERENCES `osassystem_osas_r_auth_user` (`auth_id`),
  ADD CONSTRAINT `OsasSystem_fund_fund_org_id_id_e550d0d3_fk_OsasSyste` FOREIGN KEY (`fund_org_id_id`) REFERENCES `osassystem_organization` (`org_id`),
  ADD CONSTRAINT `OsasSystem_fund_fund_room_id_id_539a3380_fk_OsasSyste` FOREIGN KEY (`fund_room_id_id`) REFERENCES `osassystem_classroom` (`room_id`);

--
-- Constraints for table `osassystem_fund_file`
--
ALTER TABLE `osassystem_fund_file`
  ADD CONSTRAINT `OsasSystem_fund_file_fund_f_head_id_id_bb7a7265_fk_OsasSyste` FOREIGN KEY (`fund_f_head_id_id`) REFERENCES `osassystem_osas_r_auth_user` (`auth_id`),
  ADD CONSTRAINT `OsasSystem_fund_file_fund_f_org_id_id_c972d039_fk_OsasSyste` FOREIGN KEY (`fund_f_org_id_id`) REFERENCES `osassystem_organization` (`org_id`),
  ADD CONSTRAINT `OsasSystem_fund_file_fund_f_room_id_id_8b934bbe_fk_OsasSyste` FOREIGN KEY (`fund_f_room_id_id`) REFERENCES `osassystem_classroom` (`room_id`),
  ADD CONSTRAINT `OsasSystem_fund_file_fund_fund_id_id_d2792c51_fk_OsasSyste` FOREIGN KEY (`fund_fund_id_id`) REFERENCES `osassystem_fund` (`fund_id`);

--
-- Constraints for table `osassystem_officer`
--
ALTER TABLE `osassystem_officer`
  ADD CONSTRAINT `OsasSystem_officer_off_org_id_id_2f9acc44_fk_OsasSyste` FOREIGN KEY (`off_org_id_id`) REFERENCES `osassystem_organization` (`org_id`),
  ADD CONSTRAINT `OsasSystem_officer_off_room_id_id_ab7dd79a_fk_OsasSyste` FOREIGN KEY (`off_room_id_id`) REFERENCES `osassystem_classroom` (`room_id`),
  ADD CONSTRAINT `OsasSystem_officer_off_stud_id_id_ff19ce3c_fk_OsasSyste` FOREIGN KEY (`off_stud_id_id`) REFERENCES `osassystem_osas_r_personal_info` (`stud_id`);

--
-- Constraints for table `osassystem_organization`
--
ALTER TABLE `osassystem_organization`
  ADD CONSTRAINT `OsasSystem_organizat_org_stud_id_id_1ad0193d_fk_OsasSyste` FOREIGN KEY (`org_stud_id_id`) REFERENCES `osassystem_osas_r_personal_info` (`stud_id`);

--
-- Constraints for table `osassystem_organization_chat`
--
ALTER TABLE `osassystem_organization_chat`
  ADD CONSTRAINT `OsasSystem_organizat_msg_head_id_id_1205b0ea_fk_OsasSyste` FOREIGN KEY (`msg_head_id_id`) REFERENCES `osassystem_osas_r_auth_user` (`auth_id`),
  ADD CONSTRAINT `OsasSystem_organizat_msg_org_id_id_6d62a5a4_fk_OsasSyste` FOREIGN KEY (`msg_org_id_id`) REFERENCES `osassystem_organization` (`org_id`),
  ADD CONSTRAINT `OsasSystem_organizat_msg_room_id_id_585d9efb_fk_OsasSyste` FOREIGN KEY (`msg_room_id_id`) REFERENCES `osassystem_classroom` (`room_id`);

--
-- Constraints for table `osassystem_org_accreditation`
--
ALTER TABLE `osassystem_org_accreditation`
  ADD CONSTRAINT `OsasSystem_org_accre_acc_org_id_id_c1227b3e_fk_OsasSyste` FOREIGN KEY (`acc_org_id_id`) REFERENCES `osassystem_organization` (`org_id`),
  ADD CONSTRAINT `OsasSystem_org_accre_acc_room_id_id_87138f7a_fk_OsasSyste` FOREIGN KEY (`acc_room_id_id`) REFERENCES `osassystem_classroom` (`room_id`);

--
-- Constraints for table `osassystem_org_concept_paper`
--
ALTER TABLE `osassystem_org_concept_paper`
  ADD CONSTRAINT `OsasSystem_org_conce_con_auth_id_id_3aa6e1d7_fk_OsasSyste` FOREIGN KEY (`con_auth_id_id`) REFERENCES `osassystem_osas_r_auth_user` (`auth_id`),
  ADD CONSTRAINT `OsasSystem_org_conce_con_org_id_id_94587bee_fk_OsasSyste` FOREIGN KEY (`con_org_id_id`) REFERENCES `osassystem_organization` (`org_id`),
  ADD CONSTRAINT `OsasSystem_org_conce_con_room_id_id_a971f8b0_fk_OsasSyste` FOREIGN KEY (`con_room_id_id`) REFERENCES `osassystem_classroom` (`room_id`),
  ADD CONSTRAINT `OsasSystem_org_conce_con_title_id_id_d6808307_fk_OsasSyste` FOREIGN KEY (`con_title_id_id`) REFERENCES `osassystem_concept_paper_title` (`title_id`);

--
-- Constraints for table `osassystem_osas_r_auth_user`
--
ALTER TABLE `osassystem_osas_r_auth_user`
  ADD CONSTRAINT `OsasSystem_osas_r_au_auth_role_id_a2af70fe_fk_OsasSyste` FOREIGN KEY (`auth_role_id`) REFERENCES `osassystem_osas_r_userrole` (`user_id`);

--
-- Constraints for table `osassystem_osas_r_personal_info`
--
ALTER TABLE `osassystem_osas_r_personal_info`
  ADD CONSTRAINT `OsasSystem_osas_r_pe_stud_course_id_id_891f0471_fk_OsasSyste` FOREIGN KEY (`stud_course_id_id`) REFERENCES `osassystem_osas_r_course` (`course_id`),
  ADD CONSTRAINT `OsasSystem_osas_r_pe_stud_role_id_355f9550_fk_OsasSyste` FOREIGN KEY (`stud_role_id`) REFERENCES `osassystem_osas_r_userrole` (`user_id`),
  ADD CONSTRAINT `OsasSystem_osas_r_pe_stud_yas_id_id_f11e0003_fk_OsasSyste` FOREIGN KEY (`stud_yas_id_id`) REFERENCES `osassystem_osas_r_section_and_year` (`yas_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
