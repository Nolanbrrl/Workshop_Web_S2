-- phpMyAdmin SQL Dump
-- version 4.1.14
-- http://www.phpmyadmin.net
--
-- Client :  127.0.0.1
-- Généré le :  Jeu 27 Juin 2024 à 22:44
-- Version du serveur :  5.6.17
-- Version de PHP :  5.5.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Base de données :  `dailynotes`
--

-- --------------------------------------------------------

--
-- Structure de la table `activity`
--

CREATE TABLE IF NOT EXISTS `activity` (
  `activity_id` int(11) NOT NULL AUTO_INCREMENT,
  `activity_name` varchar(50) NOT NULL,
  PRIMARY KEY (`activity_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=3 ;

--
-- Contenu de la table `activity`
--

INSERT INTO `activity` (`activity_id`, `activity_name`) VALUES
(1, 'golf'),
(2, 'basketball');

-- --------------------------------------------------------

--
-- Structure de la table `activity_day`
--

CREATE TABLE IF NOT EXISTS `activity_day` (
  `activity_id` int(11) NOT NULL,
  `day_id` int(11) NOT NULL,
  PRIMARY KEY (`activity_id`,`day_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Contenu de la table `activity_day`
--

INSERT INTO `activity_day` (`activity_id`, `day_id`) VALUES
(1, 1),
(2, 4);

-- --------------------------------------------------------

--
-- Structure de la table `day`
--

CREATE TABLE IF NOT EXISTS `day` (
  `day_id` int(11) NOT NULL AUTO_INCREMENT,
  `day_comment_plus` text NOT NULL,
  `day_comment_minus` text NOT NULL,
  `day_mood` int(5) NOT NULL,
  `day_drinks` int(5) NOT NULL,
  `day_sleep` int(20) NOT NULL,
  `day_date` date NOT NULL,
  `user_id` int(11) NOT NULL COMMENT 'clé étrangère',
  PRIMARY KEY (`day_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=12 ;

--
-- Contenu de la table `day`
--

INSERT INTO `day` (`day_id`, `day_comment_plus`, `day_comment_minus`, `day_mood`, `day_drinks`, `day_sleep`, `day_date`, `user_id`) VALUES
(1, 'c cool le web', 'bouh l''extreme droite ca pue', 5, 2, 7, '2024-06-25', 1),
(2, 'lébo mon chat', 'la viande c pas miam', 1, 4, 6, '2024-06-24', 1),
(3, 'on a mangé dehors avec les cop1', 'ya qqn qui a effacé le pas sur le tableau', 5, 6, 12, '2024-06-26', 1),
(4, 'loup garou ct bi1', 'colin pue du Q', 4, 4, 6, '2024-06-27', 1),
(5, 'il fé bo', 'il fé cho', 5, 4, 6, '2024-06-27', 1),
(6, 'mon pigeon est cute', 'le pigeon d''elvin est horrible', 1, 1, 6, '2024-06-27', 1),
(7, 'une chose positive que tu as retenu aujourd''hui', 'une chose négative que tu as retenue aujourd''hui', 5, 0, 13, '2024-06-27', 1),
(8, 'lkcnzlkc', 'odzajflkdnz', 3, 1, 2, '2024-06-27', 1),
(9, '', '', 3, 3, 7, '2024-06-27', 1),
(10, '', '', 3, 3, 7, '2024-06-27', 1),
(11, 'prout', '#a', 4, 5, 6, '2024-06-27', 1);

-- --------------------------------------------------------

--
-- Structure de la table `user`
--

CREATE TABLE IF NOT EXISTS `user` (
  `user_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_lastname` varchar(50) NOT NULL,
  `user_firstname` varchar(50) NOT NULL,
  `user_pseudo` varchar(50) NOT NULL,
  `user_password` varchar(50) NOT NULL,
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=3 ;

--
-- Contenu de la table `user`
--

INSERT INTO `user` (`user_id`, `user_lastname`, `user_firstname`, `user_pseudo`, `user_password`) VALUES
(1, 'Bourrel', 'Nolan', 'Nolanbrrl', 'root'),
(2, 'root', 'root', 'root', 'root');

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
