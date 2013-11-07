<?php

namespace Csg\DemoBundle\Controller;

use Csg\DataBundle\Service\GoogleDistanceClient;
use Symfony\Bundle\FrameworkBundle\Controller\Controller;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Response;

/**
 * Class DefaultController
 * @package Csg\DemoBundle\Command
 */
class DefaultController extends Controller
{
    /**
     * @return Response
     */
    public function indexAction()
    {
        /** @var $googleDistanceClient GoogleDistanceClient */
        $googleDistanceClient = $this->get('csg_data.service.google_distance_client');
        $origins = array(
            array(30.6056777, -96.3473367)
        );
        $destinations = array(
            array(30.60565222, -96.31079294)
        );
        
        $response = $googleDistanceClient->getDistanceMatrix($origins, $destinations, GoogleDistanceClient::MODE_WALKING);
        var_dump($response);
        die;
        return $this->render('CsgDemoBundle:Default:index.html.twig');
    }

    
}
