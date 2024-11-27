-- phpMyAdmin SQL Dump
-- version 4.9.5
-- https://www.phpmyadmin.net/
--
-- Servidor: localhost:8889
-- Tiempo de generación: 26-03-2021 a las 00:29:48
-- Versión del servidor: 5.7.30
-- Versión de PHP: 7.4.9

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";

--
-- Base de datos: `scheme_info`
--
CREATE DATABASE IF NOT EXISTS `scheme_info` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `scheme_info`;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `actions`
--

CREATE TABLE `actions` (
  `id_action` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `URI` varchar(10000) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `applications`
--

CREATE TABLE `applications` (
  `id_app` int(20) NOT NULL,
  `name` varchar(100) DEFAULT NULL,
  `description` varchar(1000) NOT NULL,
  `td_scheme` longtext NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `applications_containers`
--

CREATE TABLE `applications_containers` (
  `id_container` varchar(100) NOT NULL,
  `id_app` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `containers`
--

CREATE TABLE `applications_graph` 
( 
  `name_app` varchar(100) NOT NULL, 
  `structure_json` LONGTEXT NOT NULL,
  `status_json` LONGTEXT NOT NULL 
) ENGINE = InnoDB DEFAULT CHARSET=utf8;;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `containers`
--

CREATE TABLE `containers` (
  `id_container` varchar(100) NOT NULL,
  `id_long` varchar(200) NOT NULL,
  `name` varchar(100) DEFAULT NULL,
  `status` varchar(100) DEFAULT NULL,
  `image` varchar(100) DEFAULT NULL,
  `volumes` tinyint(1) NOT NULL,
  `entrypoint` varchar(1000) DEFAULT NULL,
  `platform` varchar(100) DEFAULT NULL,
  `description` varchar(1000) NOT NULL,
  `docker_port` int(11) NOT NULL,
  `host_port` int(11) NOT NULL,
  `td_scheme_pub` longtext NOT NULL,
  `td_scheme_priv` longtext NOT NULL,
  `image_p` int(11) NOT NULL,
  `volumes_p` int(11) NOT NULL,
  `status_p` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `containers_actions`
--

CREATE TABLE `containers_actions` (
  `id_container` varchar(100) NOT NULL,
  `id_action` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `containers_extras`
--

CREATE TABLE `containers_extras` (
  `name_container` varchar(500) NOT NULL,
  `type` varchar(10) NOT NULL,
  `extra` varchar(500) NOT NULL,
  `URI` varchar(10000) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `containers_utility`
--

CREATE TABLE `containers_utility` (
  `id_container` varchar(20) NOT NULL,
  `id_long` varchar(200) NOT NULL,
  `cpu_utility` float NOT NULL,
  `memory_utility` float NOT NULL,
  `network_utility` float NOT NULL,
  `fs_utility` float NOT NULL,
  `cpu_level` int(11) NOT NULL,
  `memory_level` int(11) NOT NULL,
  `network_level` int(11) NOT NULL,
  `fs_level` int(11) NOT NULL,
  `timestamp_utility` datetime NOT NULL,
  `utility_p` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `users`
--

CREATE TABLE `users` (
  `id_user` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(500) NOT NULL,
  `admin` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `actions`
--
ALTER TABLE `actions`
  ADD PRIMARY KEY (`id_action`);

--
-- Indices de la tabla `applications`
--
ALTER TABLE `applications`
  ADD PRIMARY KEY (`id_app`);

--
-- Indices de la tabla `containers`
--
ALTER TABLE `containers`
  ADD PRIMARY KEY (`id_container`);

--
-- Indices de la tabla `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id_user`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `actions`
--
ALTER TABLE `actions`
  MODIFY `id_action` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `applications`
--
ALTER TABLE `applications`
  MODIFY `id_app` int(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `users`
--
ALTER TABLE `users`
  MODIFY `id_user` int(11) NOT NULL AUTO_INCREMENT;

INSERT INTO `users` (`id_user`, `username`, `password`, `admin`) VALUES (NULL, 'mariana_hiti', '646f5f35c027495a4fd3b4308365a38c', '1');
